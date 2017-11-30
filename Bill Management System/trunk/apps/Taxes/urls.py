from django.conf.urls import url
from .views import *

app_name = 'Taxes'
urlpatterns = [
	url(r'^index/$', tax_index, name='tax_index'),
	url(r'^detail/(?P<id>[\w]+)/$', tax_detail, name='tax_detail'),
	url(r'^save/$', tax_save, name='tax_save'),
	url(r'^save/(?P<id>[0-9]+)/$', tax_save, name='tax_save'),
	url(r'^delete/(?P<id>[\w]+)/$', tax_delete, name='tax_delete'),
]