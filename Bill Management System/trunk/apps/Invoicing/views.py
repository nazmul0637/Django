from django.shortcuts import render, redirect, get_object_or_404
from BMS.utils import get_decoded_id, get_work_day
from django.http import HttpResponse
from Portfolio.models import Product, Portfolio, Purpose
from Clients.models import Client, ConcernPerson
from .models import ContractAgreement, ContractAgreementPurpose, ContractAgreementConcernPerson, BillSchedule, BillInstallmentConfig, Invoice
from .forms import ContractAgreementForm, ContractAgreementPurposeFormSet, ContractAgreementConcernPersonFormSet, BillScheduleForm, BillInstallmentConfigForm, BillScheduleFormSet
from django.forms.formsets import formset_factory
from django.db import IntegrityError, transaction
from django.contrib import messages
from datetime import datetime
from django.db.models import Sum
from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup
import re
from num2words import num2words
import json
# Create your views here.

def invoice_index(request):
	invoices = Invoice.objects.order_by('-date')
	return render(request, 'invoice/index.html', {'invoices': invoices, 'title': 'Invoice'})

def invoice_view(request, id):
	invoice = get_object_or_404(Invoice, pk = get_decoded_id(id))
	contract_agreement, bill_schedules = invoice.contract_agreement, invoice.bill_schedules.all()
	invoice_body = generate_invoice(contract_agreement, bill_schedules, str(invoice.date), invoice.subject, invoice.invoice_no)
	contex = {'invoice': invoice, 'invoice_body': str(invoice_body), 'title': 'Invoice'}
	return render(request, 'invoice/view.html', contex)

def create_invoice_no(contract_agreement, invoice_date, invoice_sequence):
	invoice_year = invoice_date.split('-')[0]
	invoice_no = 'DS/'+contract_agreement.client.short_name+'/'+contract_agreement.product.short_name+'/'+invoice_year+'-'+str(invoice_sequence)
	return invoice_no

def invoice_submit(request, id):
	invoice = get_object_or_404(Invoice, pk = get_decoded_id(id))
	invoice.status = 1
	invoice.save()
	messages.success(request, "Invoice has been successfully submitted")
	return redirect('Invoicing:invoice_view', invoice.get_encoded_id())

def invoice_save(request, id = None):
	invoice = get_object_or_404(Invoice, pk = get_decoded_id(id)) if id else None
	if request.method == 'POST':
		invoice = invoice if id else Invoice()
		invoice.subject = request.POST['subject']
		invoice.date = request.POST['invoice_date']
		bill_schedules = BillSchedule.objects.filter(pk__in = request.POST.getlist('bill_schedule'))
		total_amount = bill_schedules.aggregate(Sum('amount'))
		if id:
			invoice.bill_schedules.all().update(invoice = None)
			invoice.updated_by = request.user
		else:
			invoice.contract_agreement = ContractAgreement.objects.get(pk = int(request.POST['contract_agreement']))
			invoice.invoice_sequence = request.POST['invoice_sequence']
			invoice.created_by = request.user

		invoice.invoice_no = create_invoice_no(invoice.contract_agreement, invoice.date, invoice.invoice_sequence)
		invoice.amount = total_amount['amount__sum']
		invoice.save()
		bill_schedules.update(invoice = invoice)
		return redirect('Invoicing:invoice_view', invoice.get_encoded_id())
	if id:
		contract_agreement_purposes = invoice.contract_agreement.purposes.all()
		bill_schedules = BillSchedule.objects.filter(invoice = None, contract_agreement_purpose__in = contract_agreement_purposes, schedule_date__lte = datetime.now().date()+relativedelta(days=7)).order_by('schedule_date')
		bill_schedules = invoice.bill_schedules.all() | bill_schedules
		return render(request, 'invoice/edit.html', {'invoice': invoice, 'bill_schedules': bill_schedules, 'title': 'Edit Invoice'})
	else:
		latest_invoice = Invoice.objects.all().last()
		invoice_sequence = latest_invoice.invoice_sequence+1 if latest_invoice else 1 
		contract_agreements = ContractAgreement.objects.active()
		return render(request, 'invoice/save.html', {'contract_agreements': contract_agreements, 'invoice_sequence': invoice_sequence, 'title': 'Generate Invoice'})

def invoice_delete(request, id):
	invoice = get_object_or_404(Invoice, pk = get_decoded_id(id))
	bill_schedules = invoice.bill_schedules.all().update(invoice = None)
	invoice.delete()
	messages.success(request, "Invoice has been successfully deleted")
	return redirect('Invoicing:invoice_index')

def get_preview(request):
	if request.method == 'POST':
		contract_agreement = ContractAgreement.objects.get(pk = int(request.POST['contract_agreement']))
		bill_schedules = BillSchedule.objects.filter(pk__in = request.POST.getlist('bill_schedule'))
		invoice_no = create_invoice_no(contract_agreement, request.POST['invoice_date'], request.POST['invoice_sequence'])
		invoice_preview = generate_invoice(contract_agreement, bill_schedules, request.POST['invoice_date'], request.POST['subject'], invoice_no)
		return HttpResponse(json.dumps(str(invoice_preview)), content_type = 'application/json')

def bill_schedule_list(request, contract_agreement_id):
	contract_agreement_purposes = ContractAgreement.objects.get(pk = contract_agreement_id).purposes.all()
	bill_schedules = BillSchedule.objects.filter(invoice = None, contract_agreement_purpose__in = contract_agreement_purposes, schedule_date__lte = datetime.now().date()+relativedelta(days=7)).order_by('schedule_date')
	return render(request, 'invoice/_bill_schedule_list.html', {'bill_schedules': bill_schedules})

def contract_agreement_index(request):
	contract_agreements = ContractAgreement.objects.all()
	return render(request, 'contract_agreement/index.html', {'contract_agreements': contract_agreements, 'title': 'Contract Agreement'})

def contract_agreement_detail(request, id):
	contract_agreement = get_object_or_404(ContractAgreement, pk = get_decoded_id(id))
	contex = {
		'title': 'Contract Agreement Detail',
		'contract_agreement': contract_agreement,
	}
	return render(request, 'contract_agreement/detail.html', contex)

def contract_agreement_save(request, id = None):
	contract_agreement = get_object_or_404(ContractAgreement, pk = get_decoded_id(id)) if id else None
	contract_agreement_form = ContractAgreementForm(request.POST or None, instance = contract_agreement)

	if request.method == 'POST':
		contract_agreement_form.fields['product'].queryset = Product.objects.filter(portfolio = Portfolio.objects.get(pk = request.POST['portfolio']))
		if contract_agreement_form.is_valid():
			contract_agreement = contract_agreement_form.save(commit = False)
			contract_agreement.bank_account = contract_agreement.bank_account if contract_agreement_form.cleaned_data['mode_of_payment'] == 'Bank' else None
			contract_agreement.vat = contract_agreement.vat if contract_agreement_form.cleaned_data['is_vat_included'] else None
			if id:
				contract_agreement.updated_by = request.user
			else:
				contract_agreement.created_by = request.user

			contract_agreement_purpose_formset = ContractAgreementPurposeFormSet(request.POST, instance = contract_agreement, prefix = 'purpose')
			contract_agreement_concern_person_formset = ContractAgreementConcernPersonFormSet(request.POST, instance = contract_agreement, prefix = 'concern_person')
			if contract_agreement_purpose_formset.is_valid() and contract_agreement_concern_person_formset.is_valid():
				contract_agreement_form.save()
				contract_agreement_purpose_formset.save()
				contract_agreement_concern_person_formset.save()
				return redirect('Invoicing:bill_schedule_save', contract_agreement.get_encoded_id())
		messages.error(request, "Contract agreement has not been successfully "+ ("created" if id==None else "updated"))
	else:
		contract_agreement_purpose_formset = ContractAgreementPurposeFormSet(instance = contract_agreement, prefix = 'purpose')
		contract_agreement_concern_person_formset = ContractAgreementConcernPersonFormSet(instance = contract_agreement, prefix = 'concern_person')

	contex = {
		'contract_agreement_form': contract_agreement_form,
		'contract_agreement_purpose_formset': contract_agreement_purpose_formset,
		'contract_agreement_concern_person_formset': contract_agreement_concern_person_formset,
		'title': 'Edit Contract Agreement' if id else 'Add Contract Agreement'
	}
	return render(request, 'contract_agreement/save.html', contex)

def contract_agreement_delete(request, id):
	get_object_or_404(ContractAgreement, pk = get_decoded_id(id)).delete()
	messages.success(request, "ContractAgreement has been successfully deleted")
	return redirect('Invoicing:contract_agreement_index')

def bill_schedule_save(request, contract_agreement_id):
	contract_agreement = get_object_or_404(ContractAgreement, pk = get_decoded_id(contract_agreement_id))
	contract_agreement_purposes = contract_agreement.purposes.filter(amount_per_installment__isnull = True)
	contract_agreement_purposes_with_per_installment = contract_agreement.purposes.filter(amount_per_installment__isnull = False)
	deleted_bill_schedule_list = []
	formset_list = []
	for contract_agreement_purpose in contract_agreement_purposes:
		existing_bill_schedules = contract_agreement_purpose.bill_schedules.all()
		len_existing_bill_schedules = existing_bill_schedules.count()
		num_extra_form = contract_agreement_purpose.num_installment - contract_agreement_purpose.bill_schedules.count()
		if num_extra_form<0:
			deleted_bill_schedule_list += existing_bill_schedules[contract_agreement_purpose.num_installment:]
		
		initial = [{'particular': contract_agreement_purpose.purpose.name}]*num_extra_form
		formset = BillScheduleFormSet(request.POST or None, instance = contract_agreement_purpose, initial = initial, prefix = contract_agreement_purpose.purpose, contract_amount = contract_agreement_purpose.amount)
		formset.extra = num_extra_form
		formset_list.append({'contract_agreement_purpose': contract_agreement_purpose, 'formset': formset})
	
	bill_installment_config_form_list = []	
	for contract_agreement_purpose in contract_agreement_purposes_with_per_installment:
		if BillInstallmentConfig.objects.filter(contract_agreement_purpose = contract_agreement_purpose).exists():
			bill_installment_config = contract_agreement_purpose.bill_installment_config
			form = BillInstallmentConfigForm(request.POST or None, prefix = contract_agreement_purpose.purpose, instance = bill_installment_config)
		else:
			form = BillInstallmentConfigForm(request.POST or None, prefix = contract_agreement_purpose.purpose, initial = {'contract_agreement_purpose': contract_agreement_purpose.id, 'particular': contract_agreement_purpose})
		bill_installment_config_form_list.append({'contract_agreement_purpose': contract_agreement_purpose,  'form': form})

	if request.method == 'POST':
		if form_list_valid(bill_installment_config_form_list) and formset_list_valid(formset_list):
			bill_schedules = []
			
			for index, formset_dic in enumerate(formset_list):
				for form in formset_dic['formset']:
					bill_schedule = form.save(commit = False)
					bill_schedule.schedule_date = get_work_day(bill_schedule.schedule_date)
					bill_schedule.installment_num = index+1
					bill_schedules.append(bill_schedule)
			
			for form_dic in bill_installment_config_form_list:
				num_installment = form_dic['contract_agreement_purpose'].num_installment
				bill_installment_config = form_dic['form'].save(commit = False)
				bill_installment_config.contract_agreement_purpose = form_dic['contract_agreement_purpose']
				bill_installment_config.save()
				bill_schedule_list = bill_installment_config.bill_schedules.all()
				length = len(bill_schedule_list)
				
				if length>num_installment:
					bill_schedule_list, deleted_bill_schedule_list = bill_schedule_list[0:num_installment], deleted_bill_schedule_list + bill_schedule_list[num_installment:]
				elif length<num_installment:
					new_bill_schedule_list = [BillSchedule(contract_agreement_purpose = bill_installment_config.contract_agreement_purpose) for _ in range(num_installment-length)]
					bill_schedule_list = list(bill_schedule_list) + new_bill_schedule_list

				for i, bill_schedule in enumerate(bill_schedule_list):
					bill_schedule.installment_num = i + 1 
					bill_schedule.particular = bill_installment_config.particular
					bill_schedule.schedule_date = get_work_day(bill_installment_config.schedule_start_date + relativedelta(months = i))
					bill_schedule.amount = form_dic['contract_agreement_purpose'].amount_per_installment
					bill_schedule.bill_installment_config =  bill_installment_config
					bill_schedules.append(bill_schedule)
			
			try:
				with transaction.atomic():
					for bill_schedule in deleted_bill_schedule_list:
						bill_schedule.delete()
					for bill_schedule in bill_schedules:
						bill_schedule.save()
					return redirect('Invoicing:contract_agreement_index')
			except IntegrityError:
				messages.error(request, "Bill schedules have not been successfully created")
	
	contex = {
		'contract_agreement': contract_agreement,
		'title': 'Bill Schedule',
		'formsets': formset_list,
		'bill_installment_config_forms': bill_installment_config_form_list 
	}
	return render(request, 'bill_schedule/save.html', contex)

def formset_list_valid(formset_list):
	for formset_dic in formset_list:
		if not formset_dic['formset'].is_valid():
			return False
	return True

def form_list_valid(form_list):
	for form_dic in form_list:
		if not form_dic['form'].is_valid():
			return False
	return True

def generate_invoice(contract_agreement, bill_schedules, invoice_date, subject, invoice_no):
	template = contract_agreement.invoice_template.template_body
	soup = BeautifulSoup(template, 'html.parser')
	for v in soup.find_all(text = re.compile("[CLIENT_NAME]")):
		v.replace_with(v.replace("[CLIENT_NAME]", contract_agreement.client.name))
	for v in soup.find_all(text = re.compile("[CLIENT_ADDRESS]")):
		v.replace_with(v.replace("[CLIENT_ADDRESS]", contract_agreement.client.address))
	for v in soup.find_all(text = re.compile("[INVOICE_NO]")):
		v.replace_with(v.replace("[INVOICE_NO]", invoice_no))
	for v in soup.find_all(text = re.compile("[INVOICE_DATE]")):
		v.replace_with(v.replace("[INVOICE_DATE]", datetime.strptime(invoice_date , '%Y-%m-%d').strftime('%B %d,%Y')))
	for v in soup.find_all(text = re.compile("[SUBJECT]")):
		v.replace_with(v.replace("[SUBJECT]", subject))

	if contract_agreement.mode_of_payment == "Bank":
		bank_info = contract_agreement.bank_account
		for v in soup.find_all(text = re.compile("[ACCOUNT_NAME]")):
			v.replace_with(v.replace("[ACCOUNT_NAME]", bank_info.name_of_account))
		for v in soup.find_all(text = re.compile("[ACCOUNT_NUMBER]")):
			v.replace_with(v.replace("[ACCOUNT_NUMBER]", bank_info.account_no))
		for v in soup.find_all(text = re.compile("[BANK_NAME]")):
			v.replace_with(v.replace("[BANK_NAME]", bank_info.bank_name))
		for v in soup.find_all(text = re.compile("[BRANCH_NAME]")):
			v.replace_with(v.replace("[BRANCH_NAME]", bank_info.branch_name))
		for v in soup.find_all(text = re.compile("[BRANCH_ADRESS]")):
			v.replace_with(v.replace("[BRANCH_ADRESS]", bank_info.address))
		for v in soup.find_all(text = re.compile("[SWIFT_CODE]")):
			v.replace_with(v.replace("[SWIFT_CODE]", bank_info.swift_code))
		for v in soup.find_all(text = re.compile("[ROUTING NUMBER]")):
			v.replace_with(v.replace("[ROUTING NUMBER]", bank_info.routing_no))

	table = soup.table
	table.attrs['class'] = 'table table-bordered'
	ths = table.find_all('th')
	ths[0].attrs['class'], ths[0].attrs['width'] = 'align-center', '5%'
	ths[2].attrs['class'], ths[2].attrs['width'] = 'align-right', '15%'
	tbody = table.find('tbody')
	tbody_content = ""
	
	total_amount = 0.0
	for counter, bill_schedule in enumerate(bill_schedules):
		tbody_content+='<tr><td class="align-center">'+str(counter+1)+'</td><td>'+bill_schedule.particular+'</td><td class="align-right">'+str(bill_schedule.amount)+'</td></tr>'
		total_amount += bill_schedule.amount

	if contract_agreement.vat:
		vat_amount = total_amount*contract_agreement.vat/100
		gross_amount = total_amount + vat_amount
		tbody_content+='<tr><td colspan="2" class="align-right">Net bill amount(Excluding VAT & Tax)</td><td class="align-right">'+str(total_amount)+'</td></tr>'
		tbody_content+='<tr><td colspan="2">Add VAT '+contract_agreement.get_vat()+'</td><td class="align-right">'+str(vat_amount)+'</td></tr>'
		tbody_content+='<tr><td colspan="2" class="align-right"><b>Gross bill amount including VAT</b></td><td class="align-right"><b>'+str(gross_amount)+'</b></td></tr>'
		total_amount=gross_amount
	else:
		tbody_content+='<tr><td colspan="2" class="align-right"><b>Net bill amount</b></td><td class="align-right"><b>'+str(contract_agreement.net_amount)+'</b></td></tr>'
	
	for v in soup.find_all(text = re.compile("[ACCOUNT_DETAILS]")):
		v.replace_with(v.replace("[ACCOUNT_DETAILS]", "<b>Account detail</b>"))

	for v in soup.find_all(text = re.compile("[AMOUNT_IN_WORD]")):
		v.replace_with(v.replace("[AMOUNT_IN_WORD]", num2words(total_amount, lang = 'en_IN').capitalize()))
	
	tbody.append(BeautifulSoup(tbody_content, 'html.parser'))
	return soup

