from django.shortcuts import render, redirect, get_object_or_404
from BMS.utils import get_decoded_id
from django.contrib import messages
from .models import ExpensePurpose, Expenditure, ExpenditureDetail, Collection, CollectionDetail
from Invoicing.models import Invoice, ContractAgreementPurpose
from Portfolio.models import Product
from .forms import ExpensePurposeForm, ExpenditureForm, ExpenditureDetailFormset, CollectionForm
from django.db.models import Max, Sum
from django.db import IntegrityError, transaction
from datetime import datetime
# Create your views here.

months = {'': '', '1': 'Janaury', '2': 'February', '3': 'March', '4': 'April', '5': 'May', '6': 'June', '7': 'July', '8': 'August', '9': 'September', '10': 'October', '11': 'November', '12': 'December'}

def expense_purpose_index(request):
	expense_purposes = ExpensePurpose.objects.all()
	return render(request, 'expense_purpose/index.html', {'expense_purposes': expense_purposes, 'title': 'Expense Purpose'})

def expense_purpose_save(request, id = None):
	expense_purpose = get_object_or_404(ExpensePurpose, pk = id) if id else None
	form = ExpensePurposeForm(request.POST or None, instance = expense_purpose)
	if request.method == 'POST':
		if form.is_valid():
			expense_purpose = form.save(commit = False)
			if id:
				expense_purpose.updated_by = request.user
			else:
				expense_purpose.created_by = request.user
			expense_purpose.save()
			messages.success(request, "Expense Purpose has been successfully "+ ("updated" if id else "created"))
		else:
			messages.error(request, "Expense Purpose has not been successfully "+ ("updated" if id else "created"))

	contex = {
		'form': form,
		'title': 'Expense Purpose'
	}
	return render(request, 'modal_form/save.html', contex)

def expense_purpose_delete(request, id):
	get_object_or_404(ExpensePurpose, pk = get_decoded_id(id)).delete()
	messages.success(request, "Expense Purpose has been successfully deleted")
	return redirect('Accounts:expense_purpose_index')

def expenditure_index(request):
	expenditures = Expenditure.objects.all()
	return render(request, 'expenditure/index.html', {'expenditures': expenditures, 'title': 'Expenditure'})

def expenditure_detail(request, id):
	expenditure = get_object_or_404(Expenditure, pk = id)
	return render(request, 'expenditure/detail.html', {'expenditure': expenditure})

def get_exp_id(date):
	last_id = Expenditure.objects.all().aggregate(Max('id'))['id__max'] or 0
	date_array = str(date).split('-')
	return date_array[0] + date_array[1] + str(last_id+1)
 
def expenditure_save(request, id = None):
	expenditure = get_object_or_404(Expenditure, pk = get_decoded_id(id)) if id else None
	queryset = expenditure.expenditure_details.all() if id else ExpenditureDetail.objects.none()
	form = ExpenditureForm(request.POST or None, instance = expenditure)
	formset = ExpenditureDetailFormset(request.POST or None, queryset = queryset)
	if request.method == 'POST':
		if form.is_valid() and formset.is_valid():
			expenditure = form.save(commit = False)
			if id:
				expenditure.updated_by = request.user
			else:
				expenditure.created_by = request.user
			expenditure.save()
			instances = formset.save(commit = False)
			for instance in instances:
				instance.expenditure = expenditure
			formset.save()
			
			messages.success(request, "Expenditure has been successfully "+ ("updated" if id else "created"))
			return redirect('Accounts:expenditure_index')
		else:
			messages.error(request, "Expenditure has not been successfully "+ ("updated" if id else "created"))

	contex = {
		'form': form,
		'formset': formset,
		'title': 'Expenditure'
	}
	return render(request, 'expenditure/save.html', contex)

def expenditure_delete(request, id):
	get_object_or_404(Expenditure, pk = get_decoded_id(id)).delete()
	messages.success(request, "Expenditure has been successfully deleted")
	return redirect('Accounts:expenditure_index')

def collection_index(request):
	collections=Collection.objects.all()
	context = {
		'collections': collections,
		'title': 'Collection'
	}
	return render(request, 'collection/index.html',context)

def collection_detail(request, id):
	collection = get_object_or_404(Collection, pk = id)
	return render(request, 'collection/detail.html', {'collection': collection})

def collection_save(request):
	form = CollectionForm(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			collection = form.save(commit = False)
			collection.collected_amount = request.POST['total_paid_ammount']
			collection.collected_by = request.user
			collection.created_by = request.user
			purposes = request.POST.getlist('purpose')
			try:
				with transaction.atomic():
					collection.save()
					for purpose in purposes:
						collection_detail = CollectionDetail(collection = collection)
						collection_detail.contract_agreement_purpose = ContractAgreementPurpose.objects.get(pk = int(purpose))
						collection_detail.collected_amount = request.POST['paid_amount-'+purpose]
						collection_detail.save()
					change_invoice_status(collection)
					messages.success(request, "Collection has been successfully saved")
					return redirect('Accounts:collection_index')
			except IntegrityError:
				messages.error(request, "Collection has not been successfully savedhhhhhhhh")
		else:
			messages.error(request, "Collection has not been successfully saved")


	contex = {
		'form': form,
		'title': 'Add Collection'
	}
	return render(request, 'collection/save.html', contex)


def collection_delete(request, id):
	collection = get_object_or_404(Collection, pk = get_decoded_id(id))
	invoice = collection.invoice
	collection.delete()
	invoice.status = 1
	invoice.save()
	messages.success(request, "Collection has been successfully deleted!")
	return redirect('Accounts:collection_index')
	pass

def get_collection_details(request, invoice_id):
	invoice = get_object_or_404(Invoice, pk = invoice_id)
	bill_schedules = invoice.bill_schedules.all()
	return render(request, 'collection/_collection_details.html', {'invoice': invoice, 'bill_schedules': bill_schedules})

def change_invoice_status(collection):
	invoice=collection.invoice
	if float(invoice.amount) == float(collection.collected_amount):
		invoice.status = 3
	else :
		invoice.status = 2
	invoice.save()


def report_generate(request):
	products = Product.objects.active()
	current_year = int(datetime.now().year)
	return render(request, 'report/generate.html', {'products': products, 'title': 'Report', 'months': months, 'year_range': range(1971, 3000), 'current_year': current_year})

def get_report(request):
	if request.method == 'POST':
		product = Product.objects.get(pk = int(request.POST['product']))

		if request.POST['month']:
			incomes = CollectionDetail.objects.filter(contract_agreement_purpose__contract_agreement__product = product, collection__collection_date__year = int(request.POST['year']), collection__collection_date__month = int(request.POST['month'])).values('contract_agreement_purpose__purpose__name').annotate(Sum('collected_amount'))
			expenses = ExpenditureDetail.objects.filter(expenditure__product = product, expenditure__date__year = int(request.POST['year']), expenditure__date__month = int(request.POST['month'])).values('expense_purpose__name').annotate(Sum('amount'))
		else:
			incomes = CollectionDetail.objects.filter(contract_agreement_purpose__contract_agreement__product = product, collection__collection_date__year = int(request.POST['year'])).values('contract_agreement_purpose__purpose__name').annotate(Sum('collected_amount'))
			expenses = ExpenditureDetail.objects.filter(expenditure__product = product, expenditure__date__year = int(request.POST['year'])).values('expense_purpose__name').annotate(Sum('amount'))
		
		total_income = incomes.aggregate(Sum('collected_amount'))['collected_amount__sum']
		total_expense = expenses.aggregate(Sum('amount'))['amount__sum']
		net_profit = total_income - total_expense
		
		contex = {
			'expenses': expenses, 'product': product, 'incomes': incomes,
			'total_income': total_income, 'total_expense': total_expense, 'net_profit': net_profit,
			'year': request.POST['year'], 'month': months[request.POST['month']], 
		}

		return render(request, 'report/_report.html', contex)