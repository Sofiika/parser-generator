import os
from django.http import Http404
from django.shortcuts import render, redirect
from .models import Parser, XPath, Url
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from .parser import ParserGenerator
from .forms import XPathForm, ParserForm, UrlForm, XPathGenerateForm
import mimetypes
from django.http.response import HttpResponse
from django.conf import settings
from django import forms


# Представление главной страницы приложения
def index(request):
    parser_list = Parser.objects.all()  # список всех парсеров пользователя

    return render(
        request,
        'index.html',
        context={'parser_list': parser_list},
    )


# Представление для вывода инструкции парсера пользователю
def parser_detail_view(request, pk):
    parser_list = Parser.objects.all()  # список всех парсеров пользователя

    # Поиск парсера с нужным id
    try:
        parser_id = Parser.objects.get(pk=pk)
    except:
        raise Http404("Parser does not exist")

    # Поиск XPath и ссылок на сайты, связанных с данным парсером
    xpaths = XPath.objects.filter(parser_id=parser_id)
    url = Url.objects.filter(parser_id=parser_id)

    # Создание инструкции
    instruction = ParserGenerator.get_instruction(xpaths, url, parser_id)

    return render(
        request,
        'parser_detail.html',
        context={'parser': parser_id, 'parser_list': parser_list, 'xpaths': xpaths, 'url': url,
                 'instruction': instruction}
    )


# Представление для редактирования парсера и вывода результата парсинга
def parser_info_view(request, pk):
    # Поиск парсера по id
    try:
        parser_id = Parser.objects.get(pk=pk)
    except Parser.DoesNotExist:
        raise Http404("Parser does not exist")

    # Поиск XPath и ссылок на сайты, связанных с данным парсером
    xpaths = XPath.objects.filter(parser_id=parser_id)
    urls = Url.objects.filter(parser_id=parser_id)

    # Получение результата парсинга по инструкции
    instr = ParserGenerator.get_instruction(xpaths, urls, parser_id)
    res = ParserGenerator.parse_instruction(instr)

    return render(
        request,
        'parser_info.html',
        context={'parser': parser_id, 'xpaths': xpaths, 'urls': urls, 'results': res}
    )


# region XPath CRUD

# Представление для добавления XPath в парсер
def xpath_create(request, pk):
    # Создание XPath и добавление его к парсеру по внешнему ключу
    xpath = XPathForm().instance
    parser = Parser.objects.get(pk=pk)
    xpath.parser = parser
    form = XPathForm(instance=xpath)

    # Если форма сохраняется, то идет проверка на заполненность всех полей
    if request.method == 'POST':
        form = XPathForm(request.POST, instance=xpath)
        if form.is_valid():
            xpath_instance = form.save()

            if 'generate' in request.POST:
                return redirect('xpath-generate', xpath_instance.id)
            else:
                return redirect('parser-info', parser.id)
        else:
            form = XPathForm(instance=xpath)

    return render(request, 'xpath_form.html', {'form': form})


def xpath_generate(request, pk):
    # Создание XPath и добавление его к парсеру по внешнему ключу
    xpath = XPath.objects.get(pk=pk)
    form = XPathGenerateForm(instance=xpath)

    # Если форма сохраняется, то идет проверка на заполненность всех полей
    if request.method == 'POST':
        form = XPathGenerateForm(request.POST, instance=xpath)
        if form.is_valid():
            xpath_instance = form.save(commit=False)
            string = "//div[@class=\"" + xpath_instance.xpath_class + "\"]/" + xpath_instance.xpath_additions + "text()"
            xpath_instance.xpath_url = string
            xpath_instance.save()

            return redirect('xpath-update', xpath_instance.id)
        else:
            form = XPathGenerateForm(instance=xpath)

    return render(request, 'xpath_generate_form.html', {'form': form})


def xpath_update(request, pk):
    xpath = XPath.objects.get(pk=pk)
    form = XPathForm(instance=xpath)

    if request.method == 'POST':
        form = XPathForm(request.POST, instance=xpath)
        if form.is_valid():
            xpath_instance = form.save()

            if 'generate' in request.POST:
                return redirect('xpath-generate', xpath_instance.id)
            else:
                return redirect('parser-info', xpath_instance.parser.id)
        else:
            form = XPathForm(instance=xpath)

    return render(request, 'xpath_form.html', {'form': form})


# Представление для обновления XPath
class XPathUpdate(UpdateView):
    xpath_class = forms.CharField(required=False)
    xpath_additions = forms.CharField(required=False)

    model = XPath
    fields = ['section_name', 'xpath_url', 'xpath_method', 'xpath_class', 'xpath_additions']


# Представление для удаления XPath
class XPathDelete(DeleteView):
    model = XPath

    # Возвращение на страницу редактирования парсера после удаления
    def get_success_url(self):
        parser = self.object.parser
        return reverse_lazy('parser-info', kwargs={'pk': parser.id})


# endregion

# region Url CRUD

# Представление для добавления Url в парсер
def url_create(request, pk):
    # Создание Url и добавление его к парсеру по внешнему ключу
    url = UrlForm().instance
    parser = Parser.objects.get(pk=pk)
    url.parser = parser
    form = UrlForm(instance=url)

    # Если форма сохраняется, то идет проверка на заполненность всех полей
    if request.method == 'POST':
        form = UrlForm(request.POST, instance=url)
        if form.is_valid():
            form.save()
            return redirect('parser-info', parser.id)
        else:
            form = UrlForm(instance=url)

    return render(request, 'url_form.html', {'form': form})


# Представление для обновления ссылки на сайт
class UrlUpdate(UpdateView):
    model = Url
    fields = ['url_name']


# Представление для удаления ссылки на сайт
class UrlDelete(DeleteView):
    model = Url

    # Возвращение на страницу редактирования парсера после удаления
    def get_success_url(self):
        parser = self.object.parser
        return reverse_lazy('parser-info', kwargs={'pk': parser.id})


# endregion

# region Parser CRUD

# Представление для удаления парсера
class ParserDelete(DeleteView):
    model = Parser

    def get_success_url(self):
        return reverse_lazy('index')


# Представление для создания парсера
def parser_create(request):
    # Создание форм для парсера и Xpath и ссылки на сайт, связанных с создаваемым парсером
    parser_form = ParserForm(request.POST or None)
    xpath_form = XPathForm(request.POST or None)
    url_form = UrlForm(request.POST or None)

    # Проверка на заполнение всех полей при сохранении
    if parser_form.is_valid() and xpath_form.is_valid() and url_form.is_valid():
        # Создание объектов по заполненным полям, но пока без сохранения в базу
        parser_instance = parser_form.save(commit=False)
        xpath_instance = xpath_form.save(commit=False)
        url_instance = url_form.save(commit=False)

        # Добавление автора в парсер и сохранение парсера
        user = request.user
        parser_instance.author = user
        parser_instance.save()

        # Добавление парсера в XPath
        xpath_instance.parser = parser_instance
        xpath_instance.save()

        # Добавление парсера в ссылку на сайт
        url_instance.parser = parser_instance
        url_instance.save()

        return redirect('parser-info', parser_instance.id)

    context = {
        'parser_form': parser_form,
        'xpath_form': xpath_form,
        'url_form': url_form,
    }
    return render(request, "parser_form.html", context)


# endregion

# region Downloads

# Запрос для скачивания инструкции парсера
def download_instruction(request, pk):
    # Добавление имени файла
    filename = 'instruction.json'

    mime_type, _ = mimetypes.guess_type(filename)
    response = HttpResponse(content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename

    # Поиск парсера с нужным id
    try:
        parser_id = Parser.objects.get(pk=pk)
    except:
        raise Http404("Parser does not exist")

    # Поиск XPath и ссылок на сайты, связанных с данным парсером
    xpaths = XPath.objects.filter(parser_id=parser_id)
    url = Url.objects.filter(parser_id=parser_id)

    # Создание инструкции и запись в файл
    instruction = ParserGenerator.get_instruction(xpaths, url, parser_id)
    response.write(instruction)

    return response


# Запрос для скачивания результата парсинга в формате txt
def download_text(request, pk):
    # Добавление имени файла
    filename = 'result.txt'
    fl_path = os.path.join(settings.MEDIA_ROOT, filename)

    mime_type, _ = mimetypes.guess_type(fl_path)
    response = HttpResponse(content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename

    # Поиск парсера с нужным id
    try:
        parser_id = Parser.objects.get(pk=pk)
    except:
        raise Http404("Parser does not exist")

    # Поиск XPath и ссылок на сайты, связанных с данным парсером
    xpaths = XPath.objects.filter(parser_id=parser_id)
    url = Url.objects.filter(parser_id=parser_id)

    # Получение результата парсинга
    instruction = ParserGenerator.get_instruction(xpaths, url, parser_id)
    res = ParserGenerator.parse_instruction(instruction)

    # Сбор результата парсинга в один список
    lines = []
    for r in res:
        lines.append(r[0] + "\n")
        for r1 in r[1]:
            for r2 in r1:
                lines.append(r2 + "\n")
        lines.append("=======================================================\n")

    # Запись полученного списка в файл
    response.writelines(lines)

    return response

# endregion
