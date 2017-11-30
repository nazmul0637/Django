from django import forms
from .models import Invoicetemplate,Bankaccount,Holiday

class InvoiceTemplateForm(forms.ModelForm):
	title = forms.CharField(label = 'Title', widget = forms.TextInput(attrs = {'class': 'form-control'}))
	template_body = forms.CharField(label = 'Template', widget = forms.Textarea(attrs = {'class': 'form-control'}))
	status = forms.BooleanField(label = 'Status', help_text = 'Active', initial = True, required = False, widget = forms.widgets.CheckboxInput(attrs = {'class': 'checkbox_input'}))

	class Meta:
		model=Invoicetemplate
		fields=['title','template_body',
		'status',
		]

class BankAccountForm(forms.ModelForm):
	name_of_account = forms.CharField(label = 'Name of Account', widget = forms.TextInput(attrs = {'class': 'form-control'}))
	account_no = forms.CharField(label = 'Account Number', widget = forms.TextInput(attrs = {'class': 'form-control'}))
	bank_name = forms.CharField(label = 'Bank Name', widget = forms.TextInput(attrs = {'class': 'form-control'}))
	branch_name = forms.CharField(label = 'Branch Name', widget = forms.TextInput(attrs = {'class': 'form-control'}))
	address = forms.CharField(label = 'Address', widget = forms.TextInput(attrs = {'class': 'form-control'}))
	swift_code = forms.CharField(label = 'Swift Code', widget = forms.TextInput(attrs = {'class': 'form-control'}))
	routing_no = forms.CharField(label = 'Routing Number', widget = forms.TextInput(attrs = {'class': 'form-control'}))

	class Meta:
		model=Bankaccount
		fields=['name_of_account','account_no',
		'bank_name','branch_name','address',
		'swift_code','routing_no',
		]
class HolidayForm(forms.ModelForm):
	branch_id = forms.IntegerField(label = 'Branch ID', required = False, widget = forms.TextInput(attrs = {'class': 'form-control'}))
	holiday_date = forms.DateField(label = 'Holiday Date', widget = forms.TextInput(attrs={'class': 'form-control datetime-input'}))
	holiday_type = forms.ChoiceField(label='Holiday Type', choices=(('Weekly', 'Weekly'), ('Holiday', 'Holiday'),('Others', 'Others')), widget = forms.Select(attrs = {'class' : 'form-control select2'}), required=True)
	description = forms.CharField(label = 'Description', required = False, widget = forms.Textarea(attrs = {'class': 'form-control', 'placeholder': 'Please enter the  description'}))

	class Meta:
		model=Holiday
		fields=['branch_id', 'holiday_date', 'holiday_type', 'description',
		]
