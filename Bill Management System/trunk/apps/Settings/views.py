from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Invoicetemplate,Bankaccount,Holiday
from .forms import InvoiceTemplateForm,BankAccountForm,HolidayForm
from django.contrib import messages
from BMS.utils import get_decoded_id
from django.http import HttpResponse
from datetime import datetime

def invoice_template_index(request):
	invoice_templates = Invoicetemplate.objects.all()
	context = {
		'invoice_templates': invoice_templates,
		'title': 'Invoice Template'
	}
	return render(request, 'invoice_template/index.html', context)

def invoice_template_detail(request, id):
	invoice_template = get_object_or_404(Invoicetemplate, pk = get_decoded_id(id))
	return render(request, 'invoice_template/detail.html', {'invoice_template': invoice_template})

def invoice_template_save(request, id = None):
	invoice_template = None if id == None else Invoicetemplate.objects.get(pk = get_decoded_id(id))
	form = InvoiceTemplateForm(request.POST or None, instance = invoice_template)
	if request.method == 'POST':
		if form.is_valid():
			invoice_template = form.save(commit = False)
			if id:
				invoice_template.updated_by = request.user
			else:
				invoice_template.created_by = request.user

			invoice_template.save()

			messages.success(request, "Invoice template has been successfully "+ ("created" if id==None else "updated"))
			return redirect('Settings:invoice_template_index')
		else:
			messages.error(request, "Invoice template has not been successfully "+ ("created" if id==None else "updated"))

	context = {
		'form': form,
		'title': 'Create Template' if id==None else 'Update Template'
	}
	return render(request, 'invoice_template/save.html', context)

def invoice_template_delete(request, id):
	invoice_template = Invoicetemplate.objects.get(pk = get_decoded_id(id))
	invoice_template.delete()
	messages.success(request, "Template has been successfully deleted")
	return redirect('Settings:invoice_template_index')

def account_index(request):
	accounts = Bankaccount.objects.all()
	context = {
		'accounts': accounts,
		'title': 'Bank Accounts'
	}
	return render(request, 'account/index.html', context)

def account_detail(request, id):
	account = get_object_or_404(Bankaccount, pk = id)
	return render(request, 'account/detail.html', {'account': account})

def account_save(request, id = None):
	account = None if id == None else Bankaccount.objects.get(pk = get_decoded_id(id))
	form = BankAccountForm(request.POST or None, instance = account)
	if request.method == 'POST':
		if form.is_valid():
			account = form.save(commit = False)
			if id:
				account.updated_by = request.user
			else:
				account.created_by = request.user

			account.save()

			messages.success(request, "Account Details has been successfully "+ ("saved" if id==None else "updated"))
			return redirect('Settings:account_index')
		else:
			messages.error(request, "Account Details has not been successfully "+ ("saved" if id==None else "updated"))

	context = {
		'form': form,
		'title': 'Add Bank Account Details' if id==None else 'Update Bank Account Details'
	}
	return render(request, 'account/save.html', context)

def account_delete(request, id):
	account = Bankaccount.objects.get(pk = get_decoded_id(id))
	account.delete()
	messages.success(request, "Account Details has been successfully deleted")
	return redirect('Settings:account_index')


def holiday_index(request):
	holidays = Holiday.objects.all()
	print(Holiday.objects.filter(holiday_date = datetime.strptime('2017-01-06', '%Y-%m-%d').date()))
	context = {
		'holidays': holidays,
		'title': 'Holiday'
	}
	return render(request, 'holiday/index.html', context)

def holiday_detail(request, id):
	holiday = get_object_or_404(Holiday, pk = id)
	return render(request, 'holiday/detail.html', {'holiday': holiday})

def holiday_save(request, id = None):
	holiday = None if id == None else Holiday.objects.get(pk = get_decoded_id(id))
	form = HolidayForm(request.POST or None, instance = holiday)
	if request.method == 'POST':
		if form.is_valid():
			holiday = form.save(commit = False)
			if id:
				holiday.updated_by = request.user
			else:
				holiday.created_by = request.user

			holiday.save()

			messages.success(request, "Holiday Details has been successfully "+ ("saved" if id==None else "updated"))
			return redirect('Settings:holiday_index')
		else:
			messages.error(request, "Holiday Details has not been successfully "+ ("saved" if id==None else "updated"))

	context = {
		'form': form,
		'title': 'Add Holiday Details' if id==None else 'Update Holiday Details'
	}
	return render(request, 'holiday/save.html', context)

def holiday_delete(request, id):
	holiday = Holiday.objects.get(pk = get_decoded_id(id))
	holiday.delete()
	messages.success(request, "Holiday Details has been successfully deleted")
	return redirect('Settings:holiday_index')

