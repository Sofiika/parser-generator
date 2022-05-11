from django.contrib import admin
from .models import Parser, XPath, Url


class XPathInline(admin.TabularInline):
    model = XPath


class UrlInline(admin.TabularInline):
    model = Url


@admin.register(Parser)
class ParserAdmin(admin.ModelAdmin):
    list_display = ('parser_name', 'id', 'author')
    inlines = [XPathInline, UrlInline]


@admin.register(XPath)
class XPathAdmin(admin.ModelAdmin):
    list_display = ('section_name', 'xpath_url', 'xpath_method', 'parser', 'id')


@admin.register(Url)
class UrlAdmin(admin.ModelAdmin):
    list_display = ('url_name', 'parser')
