from django.shortcuts import render, redirect, get_object_or_404
from Portfolio.models import Product
from Clients.models import Client
from Invoicing.models import ContractAgreement
from Invoicing.models import BillSchedule
from Invoicing.models import Invoice
from django.http import HttpResponse
from django.db.models import Sum
from dateutil.relativedelta import relativedelta
from datetime import datetime

def dashboard(request):
	schedules=BillSchedule.objects.all().order_by('-schedule_date')[0:3]
	# schedules = BillSchedule.objects.filter(invoice = None, contract_agreement_purpose__in = contract_agreement_purposes, schedule_date__lte = datetime.now().date()+relativedelta(days=7)).order_by('schedule_date')
	invoices= Invoice.objects.all()
	product_count = Product.objects.all().count()
	client_count = Client.objects.all().count()
	contract_count = ContractAgreement.objects.all().count()
	receivable_amount = ContractAgreement.objects.all().aggregate(sum=Sum('net_amount'))['sum']

	context={
		'product_count': product_count,
		'client_count': client_count,
		'contract_count': contract_count,
		'receivable_amount': receivable_amount,
		'schedules': schedules,
		'invoices':invoices,
	}
	return render(request, 'dashboard.html',context)