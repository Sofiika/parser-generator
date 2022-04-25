from django.http import Http404
from django.shortcuts import render
from .models import Parser, XPath, Url
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
import requests
from urllib.request import urlopen
from lxml import etree
from sys import getdefaultencoding

# Create your views here.


def index(request):
    parser_list = Parser.objects.all()

    return render(
        request,
        'index.html',
        context={'parser_list': parser_list},
    )


def parser_detail_view(request, pk):
    parser_list = Parser.objects.all()

    try:
        parser_id = Parser.objects.get(pk=pk)
    except Parser.DoesNotExist:
        raise Http404("Parser does not exist")

    #book_id=get_object_or_404(Book, pk=pk)

    xpaths = XPath.objects.filter(parser_id=parser_id)
    url = Url.objects.filter(parser_id=parser_id)

    return render(
        request,
        'parser_detail.html',
        context={'parser': parser_id, 'parser_list': parser_list, 'xpaths': xpaths, 'url': url[0]}
    )


def parser_info_view(request, pk):
    try:
        parser_id = Parser.objects.get(pk=pk)
    except Parser.DoesNotExist:
        raise Http404("Parser does not exist")

    xpaths = XPath.objects.filter(parser_id=parser_id)
    url = Url.objects.filter(parser_id=parser_id)

    local = url[0].url_name
    response = urlopen(local)
    htmlparser = etree.HTMLParser(encoding='utf-8')
    tree = etree.parse(response, htmlparser)
    results = []
    for xpath in xpaths:
        try:
            tmp = [xpath.section_name, tree.xpath(bytes(xpath.xpath_url, 'utf-8').decode("unicode_escape"))]
        except:
            tmp = [xpath.section_name, '']

        #tree.xpath(xpath.xpath_url)
        results.append(tmp)

    return render(
        request,
        'parser_info.html',
        context={'parser': parser_id, 'xpaths': xpaths, 'url': url[0], 'results': results, 'tree': tree}
    )


class XPathCreate(CreateView):
    model = XPath
    fields = ['section_name', 'xpath_url', 'xpath_method']


class XPathUpdate(UpdateView):
    model = XPath
    fields = ['section_name', 'xpath_url', 'xpath_method']


class XPathDelete(DeleteView):
    model = XPath
    success_url = reverse_lazy('authors')
