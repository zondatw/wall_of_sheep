from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^get_more_tables/$', views.get_more_tables, name = 'get_more_tables'),
    url(r'', views.table, name = 'table'),
]
