from django.urls import path
from . import views
from django.urls import include, re_path

urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^parser/(?P<pk>[-\w]+)', views.parser_detail_view, name='parser-detail'),
    re_path(r'^parser_info/(?P<pk>[-\w]+)', views.parser_info_view, name='parser-info'),
    re_path(r'^xpath/(?P<pk>\d+)/update', views.XPathUpdate.as_view(), name='xpath-update'),
    re_path(r'^xpath/(?P<pk>[-\w]+)/delete', views.XPathDelete.as_view(), name='xpath-delete'),
    re_path(r'^xpath/create', views.XPathCreate.as_view(), name='xpath-create')
]
