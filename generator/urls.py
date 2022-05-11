from django.urls import path
from . import views
from django.urls import include, re_path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^parser/create', views.parser_create, name='parser-create'),
    re_path(r'^parser/(?P<pk>[-\w]+)/delete', views.ParserDelete.as_view(), name='parser-delete'),
    re_path(r'^parser/(?P<pk>[-\w]+)', views.parser_detail_view, name='parser-detail'),
    re_path(r'^parser_info/(?P<pk>[-\w]+)', views.parser_info_view, name='parser-info'),
    re_path(r'^xpath/(?P<pk>\d+)/update', views.XPathUpdate.as_view(), name='xpath-update'),
    re_path(r'^xpath/(?P<pk>[-\w]+)/delete', views.XPathDelete.as_view(), name='xpath-delete'),
    re_path(r'^(?P<pk>[-\w]+)/xpath/create', views.xpath_create, name='xpath-create'),
    re_path(r'^url/(?P<pk>\d+)/update', views.UrlUpdate.as_view(), name='url-update'),
    re_path(r'^url/(?P<pk>[-\w]+)/delete', views.UrlDelete.as_view(), name='url-delete'),
    re_path(r'^(?P<pk>[-\w]+)/url/create', views.url_create, name='url-create'),
    re_path(r'^download/(?P<pk>[-\w]+)', views.download_instruction, name='download-instruction'),
    re_path(r'^download_text/(?P<pk>[-\w]+)', views.download_text, name='download-text')
]
