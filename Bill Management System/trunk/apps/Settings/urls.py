from django.conf.urls import url
from .views import *

app_name='Settings'
urlpatterns = [
	url(r'^index/$', invoice_template_index, name='invoice_template_index'),
	url(r'^detail/(?P<id>[\w]+)$', invoice_template_detail, name='invoice_template_detail'),
	url(r'^save/$', invoice_template_save, name='invoice_template_save'),
	url(r'^save/(?P<id>[\w]+)$', invoice_template_save, name='invoice_template_save'),
	url(r'^delete/(?P<id>[\w]+)$', invoice_template_delete, name='invoice_template_delete'),

	url(r'^account/index/$', account_index, name='account_index'),
	url(r'^account/detail/(?P<id>[\w]+)$', account_detail, name='account_detail'),
	url(r'^account/save/$', account_save, name='account_save'),
	url(r'^account/save/(?P<id>[\w]+)$', account_save, name='account_save'),
	url(r'^account/delete/(?P<id>[\w]+)$', account_delete, name='account_delete'),

url(r'^holiday/index/$', holiday_index, name='holiday_index'),
url(r'^holiday/detail/(?P<id>[\w]+)$', holiday_detail, name='holiday_detail'),
url(r'^holiday/save/$', holiday_save, name='holiday_save'),
url(r'^holiday/save/(?P<id>[\w]+)$', holiday_save, name='holiday_save'),
url(r'^holiday/delete/(?P<id>[\w]+)$', holiday_delete, name='holiday_delete'),

]