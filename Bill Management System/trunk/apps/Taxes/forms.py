from django import forms
from .models import Tax

class TaxForm(forms.ModelForm):
	tax_type=forms.ChoiceField(label='Type', choices=(('V', 'VAT'), ('T', 'Tax')), widget = forms.Select(attrs = {'class' : 'form-control select2'}), required=True)
	#gender = forms.ChoiceField(label = 'Gender', choices = (('M', 'Male'), ('F', 'Female'), ('O', 'Others')), widget = forms.RadioSelect())
	#designation = forms.ModelChoiceField(label = 'Designation', empty_label = None, queryset = Designation.objects.all(), widget = forms.Select(attrs = {'class': 'form-control select2'}))
	name = forms.CharField(label = 'Name', widget = forms.TextInput(attrs = {'class': 'form-control'}))
	percentage=forms.DecimalField(label= 'Percentage', min_value=0, decimal_places=2,max_digits=5, widget = forms.TextInput(attrs = {'class': 'form-control'}))

	class Meta:
		model = Tax
		fields=['tax_type','name','percentage']