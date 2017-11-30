from django.conf.urls import url
from .views import *

app_name = 'Accounts'
urlpatterns = [
	url(r'^expense_purposes/index/$', expense_purpose_index, name='expense_purpose_index'),
	url(r'^expense_purposes/save/$', expense_purpose_save, name='expense_purpose_save'),
	url(r'^expense_purposes/save/(?P<id>[\w]+)$', expense_purpose_save, name='expense_purpose_save'),
	url(r'^expense_purposes/delete/(?P<id>[\w]+)$', expense_purpose_delete, name='expense_purpose_delete'),

	url(r'^expenditures/index/$', expenditure_index, name='expenditure_index'),
	url(r'^expenditures/save/$', expenditure_save, name='expenditure_save'),
	url(r'^expenditures/detail/(?P<id>[\w]+)$', expenditure_detail, name='expenditure_detail'),
	url(r'^expenditures/save/(?P<id>[\w]+)$', expenditure_save, name='expenditure_save'),
	url(r'^expenditures/delete/(?P<id>[\w]+)$', expenditure_delete, name='expenditure_delete'),

	url(r'^collections/index/$', collection_index, name='collection_index'),
	url(r'^collections/detail/(?P<id>[\w]+)$', collection_detail, name='collection_detail'),
	url(r'^collections/save/$', collection_save, name='collection_save'),
	# url(r'^collections/save/(?P<id>[\w]+)$', collection_save, name='collection_save'),
	url(r'^collections/delete/(?P<id>[\w]+)$', collection_delete, name='collection_delete'),
	url(r'^collections/collection_details/(?P<invoice_id>[\w]+)$', get_collection_details, name='get_collection_details'),

	url(r'^report/$', report_generate, name = 'report_generate'),
	url(r'^get_report/$', get_report, name = 'get_report')
]