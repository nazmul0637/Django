from django.conf.urls import url
from .views import *

app_name = 'Portfolio'
urlpatterns = [
	url(r'^index/$', portfolio_index, name='portfolio_index'),
	url(r'^detail/(?P<id>[\w]+)/$', portfolio_detail, name='portfolio_detail'),
	url(r'^save/$', portfolio_save, name='portfolio_save'),
	url(r'^save/(?P<id>[0-9]+)/$', portfolio_save, name='portfolio_save'),
	url(r'^delete/(?P<id>[\w]+)/$', portfolio_delete, name='portfolio_delete'),
	url(r'^products/index/$', product_index, name='product_index'),
	url(r'^products/detail/(?P<id>[\w]+)/$', product_detail, name='product_detail'),
	url(r'^products/save/$', product_save, name='product_save'),
	url(r'^products/save/(?P<id>[\w]+)/$', product_save, name='product_save'),
	url(r'^products/delete/(?P<id>[\w]+)/$', product_delete, name='product_delete'),
	url(r'^products/list/(?P<portfolio_id>[\w]+)/$', product_list, name='product_list'),
	url(r'^purposes/index/$', purpose_index, name='purpose_index'),
	url(r'^purposes/save/$', purpose_save, name='purpose_save'),
	url(r'^purposes/save/(?P<id>[0-9]+)/$', purpose_save, name='purpose_save'),
	url(r'^purposes/delete/(?P<id>[\w]+)/$', purpose_delete, name='purpose_delete'),
	url(r'^purposes/list/(?P<product_id>[\w]+)/$', purpose_list, name='purpose_list'),
]