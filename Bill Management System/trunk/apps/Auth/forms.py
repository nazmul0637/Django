from django import forms
from PIL import Image
from django.core.files import File
from django.contrib.auth import authenticate
from .models import User

class UserRegisterForm(forms.ModelForm):
	fullname = forms.CharField(label = 'Full Name', widget = forms.TextInput(attrs = {'class': 'form-control'}))
	username = forms.CharField(label = 'User Name', widget = forms.TextInput(attrs = {'class': 'form-control'}))
	email = forms.EmailField(label = 'Email', widget = forms.TextInput(attrs = {'class': 'form-control'}))
	password = forms.CharField(label = 'Password', min_length = 6, widget = forms.TextInput(attrs = {'class': 'form-control', 'type': 'password'}))
	confirm_password = forms.CharField(label = 'Verify Password', widget = forms.TextInput(attrs = {'class': 'form-control','type': 'password'}))
	status = forms.BooleanField(label = 'Status', initial = True, required = False, widget = forms.widgets.CheckboxInput(attrs = {'class': 'checkbox_input'}))

	class Meta:
		model = User
		fields = ['fullname','username', 'email', 'password', 'confirm_password', 'status']
	
	def clean_confirm_password(self):
		password =  self.cleaned_data.get('password')
		confirm_password = self.cleaned_data.get('confirm_password')
		if password!=confirm_password:
			raise forms.ValidationError("Passwords don't match")
		return confirm_password

	def save(self):
		user = super(UserRegisterForm, self).save(commit = False)
		user.set_password(self.cleaned_data['password'])
		return user

class UserUpdateForm(forms.ModelForm):
	fullname = forms.CharField(label = 'Full Name', widget = forms.TextInput(attrs = {'class': 'form-control'}))
	username = forms.CharField(disabled = True, label = 'User Name', widget = forms.TextInput(attrs = {'class': 'form-control'}))
	email = forms.EmailField(label = 'Email', widget = forms.TextInput(attrs = {'class': 'form-control'}))
	password = forms.CharField(required = False, label = 'Password', min_length = 6, widget = forms.TextInput(attrs = {'class': 'form-control', 'type': 'password'}))
	confirm_password = forms.CharField(required = False, label = 'Verify Password', widget = forms.TextInput(attrs = {'class': 'form-control','type': 'password'}))
	status = forms.BooleanField(label = 'Status', required = False, widget = forms.widgets.CheckboxInput(attrs = {'class': 'checkbox_input'}))
	class Meta:
		model = User
		fields = ['fullname','username', 'email', 'password', 'confirm_password', 'status']
	
	def clean_confirm_password(self):
		password =  self.cleaned_data.get('password')
		confirm_password = self.cleaned_data.get('confirm_password')
		if password!=confirm_password:
			raise forms.ValidationError("Passwords don't match")
		return confirm_password

	def save(self):
		user = User.objects.get(pk = self.instance.id)
		user.fullname = self.cleaned_data['fullname']
		user.email = self.cleaned_data['email']
		user.status = self.cleaned_data['status']
		if self.cleaned_data['password']:
			user.set_password(self.cleaned_data['password'])
		
		user.save()
		return user

class LoginForm(forms.Form):
	username = forms.CharField(label = 'Username or email', widget = forms.TextInput(attrs = {'class': 'form-control'}))
	password = forms.CharField(label = 'Password', widget = forms.TextInput(attrs = {'type': 'password', 'class': 'form-control'}))
	def clean(self):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		user = authenticate(username = username, password = password)
		if user is None:
			raise forms.ValidationError("Sorry, username or password was invalid. Please try again.")
		return self.cleaned_data

class EmailForm(forms.Form):
	email = forms.EmailField(label = 'Email', widget = forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'Enter your email address'}))
	
	def clean(self):
		cleaned_data = super(EmailForm, self).clean()
		email = self.cleaned_data.get('email')
		user = User.objects.filter(email = email)
		if not user:
			raise forms.ValidationError("Can't find that email, sorry.")
		return cleaned_data

class PasswordResetForm(forms.Form):
	new_password = forms.CharField(label = 'New Password', min_length = 6, widget = forms.TextInput(attrs = {'type': 'password', 'class': 'form-control'}))
	confirm_password = forms.CharField(label = 'Confirm Password', widget = forms.TextInput(attrs = {'type': 'password', 'class': 'form-control'}))

	def clean_confirm_password(self):
		new_password =  self.cleaned_data.get('new_password')
		confirm_password = self.cleaned_data.get('confirm_password')
		if new_password!=confirm_password:
			raise forms.ValidationError("Passwords don't match")
		return new_password
		
class ChangePasswordForm(forms.Form):
	old_password = forms.CharField(label = 'Old Password', widget = forms.TextInput(attrs = {'type': 'password', 'class': 'form-control'}))
	new_password = forms.CharField(label = 'New Password', min_length = 6, widget = forms.TextInput(attrs = {'type': 'password', 'class': 'form-control'}))
	confirm_password = forms.CharField(label = 'Confirm Password', widget = forms.TextInput(attrs = {'type': 'password', 'class': 'form-control'}))

	def __init__(self, user=None, data=None, *args, **kwargs):
		self.user = user
		super(ChangePasswordForm, self).__init__(data = data, *args, **kwargs)

	def clean_old_password(self):
		old_password = self.cleaned_data.get('old_password')
		if self.user.check_password(old_password)==False:
			raise forms.ValidationError("Old password is incorrect")
		return old_password

	def clean_confirm_password(self):
		new_password =  self.cleaned_data.get('new_password')
		confirm_password = self.cleaned_data.get('confirm_password')
		if new_password!=confirm_password:
			raise forms.ValidationError("Passwords don't match")
		return new_password

	def save(self):
		new_password = self.cleaned_data.get('new_password')
		self.user.set_password(new_password)
		self.user.save()
		return self.user

class ProfileImageForm(forms.ModelForm):
	profile_image = forms.ImageField(label = '')
	x = forms.FloatField(widget = forms.HiddenInput())
	y = forms.FloatField(widget = forms.HiddenInput())
	width = forms.FloatField(widget = forms.HiddenInput())
	height = forms.FloatField(widget = forms.HiddenInput())

	class Meta:
		model = User
		fields = ['profile_image', 'x', 'y', 'width', 'height']

	def save(self, *args, **kwargs):
		user = super(ProfileImageForm, self).save(*args, **kwargs)
		x = self.cleaned_data.get('x')
		y = self.cleaned_data.get('y')
		width = self.cleaned_data.get('width')
		height = self.cleaned_data.get('height')

		image = Image.open(user.profile_image)
		cropped_image = image.crop((x, y, x+width, y+height))
		resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
		resized_image.save(user.profile_image.path)
		return user