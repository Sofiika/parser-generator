from django.urls import path
from . import views
from django.urls import re_path

# Список ссылок приложения
urlpatterns = [
    # Ссылка на главную страницу
    path('', views.index, name='index'),
    # Ссылка на страницу регистрации
    re_path(r'^register/$', views.register, name='register'),
    # Ссылка на страницу создания парсера
    re_path(r'^parser/create', views.parser_create, name='parser-create'),
    # Ссылка на страницу удаления парсера
    re_path(r'^parser/(?P<pk>[-\w]+)/delete', views.ParserDelete.as_view(), name='parser-delete'),
    # Ссылка на страницу с инструкцией парсера
    re_path(r'^parser/(?P<pk>[-\w]+)', views.parser_detail_view, name='parser-detail'),
    # Ссылка на страницу с составляющими парсера и результатом парсинга
    re_path(r'^parser_info/(?P<pk>[-\w]+)', views.parser_info_view, name='parser-info'),
    # Ссылка на страницу редактирования XPath
    re_path(r'^xpath/(?P<pk>\d+)/update', views.xpath_update, name='xpath-update'),
    # Ссылка на страницу удаления XPath
    re_path(r'^xpath/(?P<pk>[-\w]+)/delete', views.XPathDelete.as_view(), name='xpath-delete'),
    # Ссылка на страницу создания XPath
    re_path(r'^(?P<pk>[-\w]+)/xpath/create', views.xpath_create, name='xpath-create'),
    # Ссылка на страницу генерации XPath
    re_path(r'^xpath/(?P<pk>[-\w]+)/generate', views.xpath_generate, name='xpath-generate'),
    # Ссылка на страницу редактирования ссылки на сайт
    re_path(r'^url/(?P<pk>\d+)/update', views.UrlUpdate.as_view(), name='url-update'),
    # Ссылка на страницу удаления ссылки на сайт
    re_path(r'^url/(?P<pk>[-\w]+)/delete', views.UrlDelete.as_view(), name='url-delete'),
    # Ссылка на страницу создания ссылки на сайт
    re_path(r'^(?P<pk>[-\w]+)/url/create', views.url_create, name='url-create'),
    # Ссылка для скачивания инструкции парсера
    re_path(r'^download/(?P<pk>[-\w]+)', views.download_instruction, name='download-instruction'),
    # Ссылка для скачивания результата парсинга в формате txt
    re_path(r'^download_text/(?P<pk>[-\w]+)', views.download_text, name='download-text'),
    # Ссылка для скачивания результата парсинга в формате pdf
    re_path(r'^download_pdf_text/(?P<pk>[-\w]+)', views.download_pdf_text, name='download-pdf-text')
]
