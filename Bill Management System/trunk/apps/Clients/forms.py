from django import forms
from .models import Client,ConcernPerson
from django.forms import inlineformset_factory
from django.db.models import Max

def get_code():
	code = Client.objects.all().aggregate(Max('code'))
	last_code = code['code__max'] or 999
	return last_code+1

class ClientForm(forms.ModelForm):
	name = forms.CharField(label = 'Name', widget = forms.TextInput(attrs = {'class': 'form-control'}))
	short_name = forms.CharField(label = 'Short Name', widget = forms.TextInput(attrs = {'class': 'form-control'}))
	code = forms.IntegerField(label = 'Code', disabled = True, initial = get_code, widget = forms.TextInput(attrs = {'class': 'form-control'}))
	address= forms.CharField(label = 'Address', widget = forms.TextInput(attrs = {'class': 'form-control'}))
	contact_number = forms.CharField(label = 'Contact Number', widget = forms.TextInput(attrs = {'class': 'form-control'}))
	email = forms.EmailField(label = 'Email', widget = forms.TextInput(attrs = {'class': 'form-control'}))
	description = forms.CharField(label = 'Description', required = False, widget = forms.Textarea(attrs = {'class': 'form-control', 'placeholder': 'Please enter the  description'}))
	status = forms.BooleanField(label = 'Status', help_text = 'Active', initial = True, required = False, widget = forms.widgets.CheckboxInput(attrs = {'class': 'checkbox_input'}))


	class Meta:
		model=Client
		fields=['code', 'name', 'short_name',
		'address',
		'contact_number','email',
		'description','status',
		]


class ConcernPersonForm(forms.ModelForm):
	name=forms.CharField(label = 'Name', widget = forms.TextInput(attrs = {'required': 'required'}))
	designation=forms.CharField(label ='Designation', widget = forms.TextInput(attrs = {'required': 'required'}))
	division = forms.CharField(label = 'Division', widget = forms.TextInput(attrs = {'required': 'required'}))
	contact_number = forms.CharField(label = 'Contact Number', widget = forms.TextInput(attrs = {'required': 'required'}))
	email = forms.EmailField(label = 'Email', required = False)
	status = forms.BooleanField(label = 'Status', help_text = 'Active', initial = True, required = False, widget = forms.widgets.CheckboxInput(attrs = {'class': 'checkbox_input'}))
	class Meta:
		model = ConcernPerson
		fields=['name','designation','division', 'contact_number', 'email', 'status']

ConcernPersonFormSet = inlineformset_factory(Client, ConcernPerson, form = ConcernPersonForm, can_delete = True, min_num = 1, extra = 0)