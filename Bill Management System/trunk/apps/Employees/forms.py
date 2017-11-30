from django import forms
from PIL import Image
from django.core.files import File
from .models import Employee,Designation
from django.conf import settings

class DesignationCreationForm(forms.ModelForm):
	title=forms.CharField(label = 'Designation', widget = forms.TextInput(attrs = {'class': 'form-control'}))
	status = forms.BooleanField(label = 'Status', initial = True, required = False, widget = forms.widgets.CheckboxInput(attrs = {'class': 'checkbox_input'}))
	class Meta:
		model = Designation
		fields=['title','status',]

class EmployeeCreationForm(forms.ModelForm):
	name = forms.CharField(label = 'Name', widget = forms.TextInput(attrs = {'class': 'form-control'}))
	employee_id = forms.CharField(label = 'Employee id', widget = forms.TextInput(attrs = {'class': 'form-control'}))
	designation = forms.ModelChoiceField(label = 'Designation', queryset = Designation.objects.active(), widget = forms.Select(attrs = {'class': 'form-control select2'}))
	father_name = forms.CharField(label = "Father's Name", widget = forms.TextInput(attrs = {'class': 'form-control'}))
	mother_name = forms.CharField(label = "Mother's Name", widget = forms.TextInput(attrs = {'class': 'form-control'}))
	present_address= forms.CharField(label = 'Present Address', widget = forms.TextInput(attrs = {'class': 'form-control'}))
	permanent_address =forms.CharField(label = 'Permanent Address', widget = forms.TextInput(attrs = {'class': 'form-control'}))
	gender = forms.ChoiceField(label = 'Gender', choices = (('M', 'Male'), ('F', 'Female'), ('O', 'Others')), widget = forms.RadioSelect(attrs = {'id': 'inline_radio'}))
	contact_number = forms.CharField(label = 'Contact Number', widget = forms.TextInput(attrs = {'class': 'form-control'}))
	email = forms.EmailField(label = 'Email', widget = forms.TextInput(attrs = {'class': 'form-control'}))
	starting_salary = forms.FloatField(label = 'Starting salary', required = False, widget = forms.TextInput(attrs = {'class': 'form-control', 'type': 'number', 'step': 'any', 'min': '1.0'}))
	current_salary = forms.FloatField(label = 'Current salary', required = False, widget = forms.TextInput(attrs = {'class': 'form-control', 'type': 'number', 'step': 'any', 'min': '1.0'}))
	national_id = forms.CharField(label = 'National ID', required = False, widget = forms.TextInput(attrs = {'class': 'form-control'}))
	status = forms.BooleanField(label = 'Status', initial = True, required = False, widget = forms.widgets.CheckboxInput(attrs = {'class': 'checkbox_input'}))
	date_of_birth = forms.DateField(widget = forms.TextInput(attrs={'class': 'form-control datetime-input'}))
	date_of_joining = forms.DateField(widget = forms.TextInput(attrs={'class': 'form-control datetime-input'}))

	class Meta:
		model=Employee
		fields=['name', 'employee_id', 'designation','father_name',
		'mother_name','present_address','permanent_address',
		'gender','date_of_birth','contact_number','email','date_of_joining',
		'starting_salary','current_salary','national_id','status',
		]

class ProfileImageForm(forms.ModelForm):
	profile_image = forms.ImageField(label = '')
	x = forms.FloatField(widget = forms.HiddenInput())
	y = forms.FloatField(widget = forms.HiddenInput())
	width = forms.FloatField(widget = forms.HiddenInput())
	height = forms.FloatField(widget = forms.HiddenInput())

	class Meta:
		model = Employee
		fields = ['profile_image', 'x', 'y', 'width', 'height']

	def save(self, *args, **kwargs):
		employee = super(ProfileImageForm, self).save(*args, **kwargs)
		x = self.cleaned_data.get('x')
		y = self.cleaned_data.get('y')
		width = self.cleaned_data.get('width')
		height = self.cleaned_data.get('height')

		image = Image.open(employee.profile_image)
		cropped_image = image.crop((x, y, x+width, y+height))
		resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
		resized_image.save(employee.profile_image.path)
		return employee






