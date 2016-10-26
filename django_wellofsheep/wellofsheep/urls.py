from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'', views.table),
    url(r'^get_more_tables/$', views.get_more_tables, name = 'get_more_tables'),
]
