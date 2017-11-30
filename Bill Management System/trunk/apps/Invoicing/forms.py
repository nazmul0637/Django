from django import forms
from django.forms import inlineformset_factory, BaseInlineFormSet
from django.forms.formsets import BaseFormSet
from .models import ContractAgreement, ContractAgreementPurpose, ContractAgreementConcernPerson, BillSchedule, BillInstallmentConfig
from Clients.models import Client, ConcernPerson
from Portfolio.models import Product, Portfolio, Purpose
from Settings.models import Bankaccount, Invoicetemplate

MODE_OF_PAYMENT_CHOICES = (('', '---------'), ('Cash', 'Cash'), ('Bank', 'Bank'), ('DD', 'DD'), ('TT', 'TT'))

class ContractAgreementForm(forms.ModelForm):
	client = forms.ModelChoiceField(label = 'Client', queryset = Client.objects.active(), widget = forms.Select(attrs = {'class': 'select2'}))
	portfolio = forms.ModelChoiceField(label = 'Portfolio', queryset = Portfolio.objects.active(), widget = forms.Select(attrs = {'class': 'select2'}))
	product = forms.ModelChoiceField(label = 'Product/Project', queryset = Product.objects.none(), widget = forms.Select(attrs = {'class': 'select2'}))
	agreement_date = forms.DateField(label = 'Agreement Date', widget = forms.TextInput(attrs = {'class': 'form-control datetime-input'}))
	net_amount = forms.FloatField(label = 'Net Amount Excluding VAT', widget = forms.TextInput(attrs = {'class': 'form-control align-right', 'type': 'number', 'min': '1.0', 'step': 'any'}))
	mode_of_payment = forms.ChoiceField(label = 'Mode of Payment', choices = MODE_OF_PAYMENT_CHOICES, widget = forms.Select(attrs = {'class': 'form-control select2'}))
	bank_account = forms.ModelChoiceField(label = 'Bank Account', required = False, queryset = Bankaccount.objects.all(), widget = forms.Select(attrs = {'class': 'select2'}))
	invoice_template = forms.ModelChoiceField(label = 'Invoice Template', queryset = Invoicetemplate.objects.all(), widget = forms.Select(attrs = {'class': 'select2'}))
	is_vat_included = forms.BooleanField(label = 'Is VAT included', required = False, initial = False)
	vat = forms.FloatField(label = 'VAT', required = False, widget = forms.TextInput(attrs = {'class': 'form-control align-right', 'type': 'number', 'min': '0', 'step': 'any'}))

	class Meta:
		model = ContractAgreement
		fields = ['client', 'portfolio', 'product', 'agreement_date', 'mode_of_payment', 'bank_account', 'invoice_template', 'net_amount', 'vat']

	def __init__(self, *args, **kwargs):
		super(ContractAgreementForm, self).__init__(*args, **kwargs)
		instance = kwargs['instance']
		if instance:
			if instance.vat:
				self.fields['is_vat_included'].initial = True
				self.fields['vat'].required = True
			self.fields['portfolio'].initial = instance.product.portfolio
			self.fields['product'].queryset = instance.product.portfolio.products.all()

class ContractAgreementConcernPersonForm(forms.ModelForm):
	concern_person = forms.ModelChoiceField(label = 'Concern Person', queryset = ConcernPerson.objects.none(), widget = forms.Select(attrs = {'class': 'form-control', 'required': 'required'}))
	concern_person_type = forms.ChoiceField(label = 'Type', choices = (('', '---------'), ('first', 'First'), ('second', 'Second'), ('third', 'Third')), widget = forms.Select(attrs = {'class': 'form-control', 'required': 'required'}))

	class Meta:
		model = ContractAgreementConcernPerson
		fields = ['concern_person', 'concern_person_type']

class BaseConcernPersonFormSet(BaseInlineFormSet):
	def __init__(self, *args, **kwargs):
		super(BaseConcernPersonFormSet, self).__init__(*args, **kwargs)
		instance = kwargs['instance']
		if instance:
			for form in self.forms:
				form.fields['concern_person'].queryset = instance.client.concern_persons.all()

	def clean(self):
		super(BaseConcernPersonFormSet, self).clean()
		concern_persons = []
		for form in self.forms:
			if form.cleaned_data:
				if form.cleaned_data['concern_person'] in concern_persons:
					raise forms.ValidationError('Same ConcernPerson has been included more than one time')
				else:
					concern_persons.append(form.cleaned_data['concern_person'])

ContractAgreementConcernPersonFormSet = inlineformset_factory(ContractAgreement, ContractAgreementConcernPerson, form = ContractAgreementConcernPersonForm, formset = BaseConcernPersonFormSet, can_delete = True, min_num = 1, extra = 0)

class ContractAgreementPurposeForm(forms.ModelForm):
	purpose = forms.ModelChoiceField(label = 'Purpose Name', queryset = Purpose.objects.none(), widget = forms.Select(attrs = {'class': 'form-control', 'required': 'required'}))
	amount_per_installment = forms.FloatField(label = 'Amount Per Installment', required = False, widget = forms.TextInput(attrs = {'class': 'form-control align-right', 'type': 'number', 'min': '1.0', 'onchange': 'changeTotal(this)'}))
	amount = forms.FloatField(label = 'Total Amount', widget = forms.TextInput(attrs = {'class': 'form-control align-right','type': 'number', 'min': '1.0', 'step': 'any', 'required': 'required'}))
	num_installment = forms.IntegerField(label = 'Number of installment', widget = forms.TextInput(attrs = {'class': 'form-control', 'type': 'number', 'min': '1', 'required': 'required', 'onchange': 'changeTotal(this)'}))

	class Meta:
		model = ContractAgreementPurpose
		fields = ['purpose', 'num_installment', 'amount_per_installment', 'amount']

class BasePurposeFormSet(BaseInlineFormSet):
	def __init__(self, *args, **kwargs):
		super(BasePurposeFormSet, self).__init__(*args, **kwargs)
		instance = kwargs['instance']
		if instance:
			for form in self.forms:
				form.fields['purpose'].queryset = instance.product.purposes.all()
	def clean(self):
		super(BasePurposeFormSet, self).clean()
		purposes = []
		total_amount = 0.0
		for form in self.forms:
			if form.cleaned_data:
				total_amount += form.cleaned_data['amount']
				if form.cleaned_data['purpose'] in purposes:
					raise forms.ValidationError('Same purpose has been included more than one time')
				else:
					purposes.append(form.cleaned_data['purpose'])
		# if total_amount < self.instance.net_amount:
		# 	raise forms.ValidationError('Total amount for purposes is short by '+str(self.instance.net_amount-total_amount)+' amount from net contract amount')
		# elif total_amount > self.instance.net_amount:
		# 	raise forms.ValidationError('Total amount for purposes exceeds by '+str(total_amount-self.instance.net_amount)+' amount from net contract amount')	

ContractAgreementPurposeFormSet = inlineformset_factory(ContractAgreement, ContractAgreementPurpose, form = ContractAgreementPurposeForm, can_delete = True, formset = BasePurposeFormSet, min_num = 1, extra =0)


class BillInstallmentConfigForm(forms.ModelForm):
	installment_type = forms.ChoiceField(label = 'Installment Type', choices = (('', '----------'), (1, 'Monthly'), (4, 'Quarterly'), (6, 'Half Yearly'), (12, 'Yearly')), widget = forms.Select())
	particular = forms.CharField(label = 'Particular', widget = forms.TextInput())
	use_sequence = forms.BooleanField(label = 'Use Sequence in particular', required = False, initial = False, widget = forms.CheckboxInput(attrs = {'class': 'checkbox_input'}))
	schedule_start_date = forms.DateField(label = 'Schedule Start Date', widget = forms.TextInput(attrs = {'class': 'datetime-input'}))

	class Meta:
		model = BillInstallmentConfig
		fields = ['installment_type', 'particular', 'use_sequence', 'schedule_start_date']

class BillScheduleForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(BillScheduleForm, self).__init__(*args, **kwargs)
	particular = forms.CharField(label = 'Particular', widget = forms.TextInput(attrs = {'required': 'required'}))
	schedule_date = forms.DateField(label = 'Schedule Date', widget = forms.TextInput(attrs = {'class': 'datetime-input', 'required': 'required'}))
	amount = forms.FloatField(label = 'Amount', widget = forms.TextInput(attrs = {'class': 'align-right','type': 'number', 'min': '1.0', 'step': 'any', 'required': 'required'}))

	class Meta:
		model = BillSchedule
		fields = ['particular', 'schedule_date', 'amount']

class BaseBillScheduleFormSet(BaseInlineFormSet):
	def __init__(self, *args, **kwargs):
		self.contract_amount = kwargs.pop('contract_amount', None)
		super(BaseBillScheduleFormSet, self).__init__(*args, **kwargs)

	def clean(self):
		# if any(self.errors):
		# 	return
		super(BaseBillScheduleFormSet, self).clean()
		amount = 0.0
		for form in self.forms:
			if form.cleaned_data:
				amount += form.cleaned_data['amount']
		if self.contract_amount != amount:
			raise forms.ValidationError('Total amount of installments is not same as total contract amount!')

BillScheduleFormSet = inlineformset_factory(ContractAgreementPurpose, BillSchedule, form = BillScheduleForm, formset = BaseBillScheduleFormSet, min_num = 0, extra = 0, can_delete = False)








