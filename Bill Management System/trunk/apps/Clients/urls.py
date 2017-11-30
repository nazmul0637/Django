from django.conf.urls import url
from .views import *

app_name='Clients'
urlpatterns = [
url(r'^index/$', client_index, name='client_index'),
url(r'^detail/(?P<id>[\w]+)$', client_detail, name='client_detail'),
url(r'^save/$', client_save, name='client_save'),
url(r'^save/(?P<id>[\w]+)$', client_save, name='client_save'),
url(r'^delete/(?P<id>[\w]+)$', client_delete, name='client_delete'),
url(r'^concern_persons/list/(?P<client_id>[\w]+)$', concern_person_list, name='concern_person_list'),
]