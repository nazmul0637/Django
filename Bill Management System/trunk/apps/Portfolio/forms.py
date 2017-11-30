from django import forms
from .models import Portfolio, Product, Purpose
from Employees.models import Employee

class PortfolioCreationForm(forms.ModelForm):
	name = forms.CharField(label = 'Name', widget = forms.TextInput(attrs = {'class': 'form-control'}))
	description = forms.CharField(label = 'Description', required = False, widget = forms.Textarea(attrs = {'class': 'form-control', 'placeholder': 'Please enter the  description'}))
	concern_persons = forms.ModelMultipleChoiceField(label = 'Concern Persons',  queryset = Employee.objects.active(), widget = forms.SelectMultiple(attrs = {'class': 'form-control select2'}))
	status = forms.BooleanField(label = 'Status', initial = True, required = False, widget = forms.widgets.CheckboxInput(attrs = {'class': 'checkbox_input'}))
	start_date = forms.DateField(label = 'Start Date', widget = forms.TextInput(attrs={'class': 'form-control datetime-input'}))

	class Meta:
		model = Portfolio
		fields = ['name', 'start_date', 'concern_persons', 'description', 'status']

class ProductCreationForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(ProductCreationForm, self).__init__(*args, **kwargs)
		if self.instance:
			for product_purpose in self.instance.productpurpose_set.all():
				self.fields['purpose_'+str(product_purpose.purpose.id)]= forms.FloatField(label = product_purpose.purpose.name, required = False, widget = forms.TextInput(attrs = {'class': 'form-control', 'value': product_purpose.amount, 'type': 'number', 'step': 'any', 'min': '1.0'}))

	name = forms.CharField(label = 'Name', widget = forms.TextInput(attrs = {'class': 'form-control'}))
	short_name = forms.CharField(label = 'Short Name', widget = forms.TextInput(attrs = {'class': 'form-control'}))
	product_type=forms.ChoiceField(label='Type', choices=(('Project', 'Project'), ('Product', 'Product')), widget = forms.RadioSelect(attrs = {'id': 'inline_radio'}))
	concern_persons = forms.ModelMultipleChoiceField(label = 'Concern Persons',  queryset = Employee.objects.active(), widget = forms.SelectMultiple(attrs = {'class': 'form-control select2'}))
	description = forms.CharField(label = 'Description', required = False, widget = forms.Textarea(attrs = {'class': 'form-control', 'placeholder': 'Please enter the  description'}))
	portfolio = forms.ModelChoiceField(label = 'Portfolio', queryset = Portfolio.objects.all(), widget = forms.Select(attrs = {'class': 'form-control select2'}))
	purposes = forms.ModelMultipleChoiceField(label = 'Purposes', queryset = Purpose.objects.all(), widget = forms.SelectMultiple(attrs = {'class': 'form-control select2'}))
	status = forms.BooleanField(label = 'Status', initial = True, required = False, widget = forms.widgets.CheckboxInput(attrs = {'class': 'checkbox_input'}))
	start_date = forms.DateField(label = 'Start Date', widget = forms.TextInput(attrs={'class': 'form-control datetime-input'}))

	class Meta:
		model = Product
		fields = ['name', 'short_name', 'product_type', 'portfolio', 'concern_persons', 'start_date', 'description', 'status', 'purposes']

class PurposeCreationForm(forms.ModelForm):
	name = forms.CharField(label = 'Name', widget = forms.TextInput(attrs = {'class': 'form-control'}))
	description = forms.CharField(label = 'Description', required = False, widget = forms.Textarea(attrs = {'class': 'form-control', 'placeholder': 'Please enter the  description'}))
	status = forms.BooleanField(label = 'Status', initial = True, required = False, widget = forms.widgets.CheckboxInput(attrs = {'class': 'checkbox_input'}))

	class Meta:
		model = Purpose
		fields = ['name', 'description', 'status']
 