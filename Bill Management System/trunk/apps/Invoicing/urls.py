from django.conf.urls import url
from .views import *

app_name='Invoicing'
urlpatterns = [
	url(r'^index/$', invoice_index, name = 'invoice_index'),
	url(r'^view/(?P<id>[\w]+)/$', invoice_view, name = 'invoice_view'),
	url(r'^save/$', invoice_save, name = 'invoice_save'),
	url(r'^save/(?P<id>[\w]+)/$', invoice_save, name = 'invoice_save'),
	url(r'^submit/(?P<id>[\w]+)/$', invoice_submit, name = 'invoice_submit'),
	url(r'^preview/$', get_preview, name = 'get_preview'),
	url(r'^delete/(?P<id>[\w]+)/$', invoice_delete, name = 'invoice_delete'),
	url(r'^contract_agreements/index/$', contract_agreement_index, name = 'contract_agreement_index'),
	url(r'^contract_agreements/detail/(?P<id>[\w]+)/$', contract_agreement_detail, name = 'contract_agreement_detail'),
	url(r'^contract_agreements/save/$', contract_agreement_save, name = 'contract_agreement_save'),
	url(r'^contract_agreements/save/(?P<id>[\w]+)/$', contract_agreement_save, name = 'contract_agreement_save'),
	url(r'^contract_agreements/delete/(?P<id>[\w]+)/$', contract_agreement_delete, name = 'contract_agreement_delete'),
	url(r'^bill_schedule/save/(?P<contract_agreement_id>[\w]+)/$', bill_schedule_save, name = 'bill_schedule_save'),
	url(r'^bill_schedule/list/(?P<contract_agreement_id>[\w]+)/$', bill_schedule_list, name = 'bill_schedule_list'),
]