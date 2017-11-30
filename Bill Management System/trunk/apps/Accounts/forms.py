from django import forms
from .models import ExpensePurpose, Expenditure, ExpenditureDetail, Collection
from django.forms import inlineformset_factory, BaseInlineFormSet, modelformset_factory
from Invoicing.models import Invoice
from Portfolio.models import Product
from django.db.models import Max

def get_expense_purpose_code():
	code = ExpensePurpose.objects.all().aggregate(Max('code'))
	last_code = code['code__max'] or 999
	return last_code+1

def get_seq_num():
	last_seq_num = Expenditure.objects.all().aggregate(Max('seq_num'))
	last_seq_num = last_seq_num['seq_num__max'] or 0
	return last_seq_num+1

class ExpensePurposeForm(forms.ModelForm):
	name = forms.CharField(label = 'Name', widget = forms.TextInput(attrs = {'class': 'form-control'}))
	code = forms.IntegerField(label = 'code', disabled = True, initial = get_expense_purpose_code, widget = forms.TextInput(attrs = {'class': 'form-control'}))
	description = forms.CharField(label = 'Description', required = False, widget = forms.Textarea(attrs = {'class': 'form-control'}))

	class Meta:
		model = ExpensePurpose
		fields = ['name', 'code', 'description']

class ExpenditureForm(forms.ModelForm):
	product = forms.ModelChoiceField(label = 'Product/Project', queryset = Product.objects.active(), widget = forms.Select(attrs = {'class': 'form-control select2'}))
	seq_num = forms.IntegerField(initial = get_seq_num, widget = forms.TextInput(attrs = {'hidden': 'hidden'}))
	exp_id = forms.CharField(label = 'Expense ID', widget = forms.TextInput(attrs = {'class': 'form-control', 'readonly': 'readonly'}))
	date = forms.DateField(label = 'Date', widget = forms.TextInput(attrs = {'class': 'form-control datetime-input'}))
	description = forms.CharField(label = 'Description', required = False, widget = forms.Textarea(attrs = {'class': 'form-control'}))

	class Meta:
		model = Expenditure
		fields = ['product', 'seq_num', 'exp_id','date','description']

class ExpenditureDetailForm(forms.ModelForm):
	expense_purpose = forms.ModelChoiceField(label = 'Purpose', queryset = ExpensePurpose.objects.all(), widget = forms.Select(attrs = {'class': 'form-control'}))
	amount = forms.FloatField(label = 'Amount', widget = forms.TextInput(attrs = {'class': 'form-control align-right', 'type': 'number', 'min': '1.0'}))

	class Meta:
		model = ExpenditureDetail
		fields = ['expense_purpose', 'amount']

ExpenditureDetailFormset = modelformset_factory(ExpenditureDetail, form = ExpenditureDetailForm, min_num = 1, extra = 0, can_delete = True)

class CollectionForm(forms.ModelForm):
	invoice = forms.ModelChoiceField(label='Invoice', empty_label = "Select an invoice", queryset=Invoice.objects.filter(status = 1), widget=forms.Select(attrs = {'class': 'select2'}))
	collection_date = forms.DateField(label = 'Collection Date', widget = forms.TextInput(attrs= {'class': 'form-control datetime-input'}))
	description = forms.CharField(label = 'Description', required = False, widget = forms.Textarea(attrs = {'class': 'form-control'}))
	class Meta:
		model = Collection
		fields=['invoice','collection_date','description',]