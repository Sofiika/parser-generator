from django.db import models
import uuid
from django.contrib.auth.models import User
from django.urls import reverse


# Модель XPath
class XPath(models.Model):
    # Словарь методов обработки XPath
    LOAN_METHOD = (
        ("article_text", "process_article_text"),  # Метод для вывода полученных кусков текста в одну строку
        ("singular_item", "process_singular_item"),  # Метод для вывода одного элемента
        ("external_links", "process_external_links"),  # Метод для вывода ссылки
        ("array_item", "process_array_item"),  # # Метод для вывода полученных кусков текста в несколько строк
    )
    # Название раздела для пользователя
    section_name = models.TextField(null=True, default='section 1',
                                    help_text="<span class=\"tooltip\">?<span class=\"tooltiptext\">Enter section name</span></span>")
    # Формула XPath
    xpath_url = models.TextField(null=True, default='',
                                 help_text="<span class=\"tooltip\">?<span class=\"tooltiptext\">Enter XPath formula</span></span>")
    xpath_method = models.CharField(max_length=22, choices=LOAN_METHOD, default="article_text")  # Метод обработки XPath
    xpath_class = models.TextField(default='', null=True)  # Класс XPath (используется для генерации)
    xpath_additions = models.TextField(default='', null=True)  # Добавления XPath (используется для генерации)
    parser = models.ForeignKey('Parser', to_field='id', on_delete=models.CASCADE, null=True) # Парсер, привзянный к XPath

    # Строка для краткого представления XPath
    def __str__(self):
        return self.section_name + self.xpath_url

    # Передает ссылку на страницу редактирования парсера с аргументом id
    def get_absolute_url_update(self):
        return reverse('xpath-update', args=[str(self.id)])

    # Передает ссылку на страницу удаления парсера с аргументом id
    def get_absolute_url_delete(self):
        return reverse('xpath-delete', args=[str(self.id)])

    # Передает ссылку на страницу редактирования парсера с аргументом id привязанного парсера (для перехода после создания)
    def get_absolute_url(self):
        return reverse('parser-info', args=[str(self.parser.id)])


# Модель ссылки на сайт
class Url(models.Model):
    url_name = models.TextField(help_text="<span class=\"tooltip\">?<span class=\"tooltiptext\">Enter link to website</span></span>")  # Ссылка на сайт
    parser = models.ForeignKey('Parser', to_field='id', on_delete=models.CASCADE, null=True)  # Парсер, привязанный к ссылке

    # Строка для краткого представления ссылки
    def __str__(self):
        return self.url_name

    # Передает ссылку на страницу редактирования url с аргументом id
    def get_absolute_url_update(self):
        return reverse('url-update', args=[str(self.id)])

    # Передает ссылку на страницу удаления url с аргументом id
    def get_absolute_url_delete(self):
        return reverse('url-delete', args=[str(self.id)])

    # Передает ссылку на страницу редактирования парсера с аргументом id привязанного парсера (для перехода после создания)
    def get_absolute_url(self):
        return reverse('parser-info', args=[str(self.parser.id)])


# Модель парсера
class Parser(models.Model):
    parser_name = models.TextField(null=True)  # Имя парсера
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)  # id парсера
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Автор парсера

    # Строка для краткого представления парсера
    def __str__(self):
        return self.parser_name

    # Передает ссылку на страницу с инструкцией парсера с аргументом id
    def get_absolute_url(self):
        return reverse('parser-detail', args=[str(self.id)])

    # Передает ссылку на страницу редактирования парсера с аргументом id
    def get_absolute_url_info(self):
        return reverse('parser-info', args=[str(self.id)])

    # Передает ссылку на страницу создания XPath с аргументом id
    def get_absolute_url_add_xpath(self):
        return reverse('xpath-create', args=[str(self.id)])

    # Передает ссылку на страницу создания url с аргументом id
    def get_absolute_url_add_url(self):
        return reverse('url-create', args=[str(self.id)])

    # Передает ссылку на страницу удаления парсера с аргументом id
    def get_absolute_url_delete(self):
        return reverse('parser-delete', args=[str(self.id)])

    # Передает ссылку на страницу скачивания инструкции с аргументом id
    def get_absolute_url_download(self):
        return reverse('download-instruction', args=[str(self.id)])

    # Передает ссылку на страницу скачивания результата в формате txt с аргументом id
    def get_absolute_url_download_text(self):
        return reverse('download-text', args=[str(self.id)])

    # Передает ссылку на страницу скачивания результата в формате pdf с аргументом id
    def get_absolute_url_download_pdf_text(self):
        return reverse('download-pdf-text', args=[str(self.id)])
