from BMS.utils import get_decoded_id, get_encoded_id
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, update_session_auth_hash
from django.contrib import messages
from django.conf import settings
from .models import User
from .forms import UserRegisterForm, UserUpdateForm, LoginForm, ChangePasswordForm, ProfileImageForm, PasswordResetForm, EmailForm
from django.core.mail import send_mail, BadHeaderError
import os
from datetime import datetime
from django.utils import timezone
from dateutil.relativedelta import relativedelta
import time
# Create your views here.

def login(request):
	form = LoginForm(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			user = authenticate(username = form.cleaned_data['username'], password = form.cleaned_data['password'])
			auth_login(request, user)
			if not request.POST.get('remember_me', False):
				request.session.set_expiry(0)
			return redirect(settings.HOME_URL)
	contex = {
		'form': form
	}
	return render(request, 'auth/login.html', contex)

def logout(request):
	auth_logout(request)
	return redirect('Auth:login')

def forget_password(request):
	form = EmailForm(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			email = form.cleaned_data['email']
			user = User.objects.get(email = email)
			token = get_encoded_id(round(time.time()*1000))
			recovery_url = request.build_absolute_uri(reverse('Auth:reset_password', args = [token]))
			user.recovery_token = token
			user.save()
			try:
				send_mail("Reset Password", "Hello, "+user.fullname+", follow this link to recover your password: "+recovery_url+" If you don’t use this link within 24 hours, it will expire", "Invoice Manager", [email])
			except BadHeaderError:
				return HttpResponse('Invalid header found.')

			return render(request, 'auth/send_email_success.html')

	return render(request, 'auth/send_email.html', {'form': form})

def reset_password(request, token):
	users = User.objects.filter(recovery_token = token)
	if users:
		user = users[0]
		if user.recovery_token_time+relativedelta(days = 1)<timezone.now():
			messages.error(request, "Your recovery link expired. Send recovery mail again")
			return redirect('Auth:forget_password')
	else:
		messages.error(request, "Your recovery link is invalid. Send recovery mail again")
		return redirect('Auth:forget_password')

	form = PasswordResetForm(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			users[0].set_password(form.cleaned_data['new_password'])
			users[0].save()
			return redirect('Auth:login')
	return render(request, 'auth/reset_password.html', {'form': form})

def change_password(request):
	form = ChangePasswordForm(user = request.user, data = request.POST or None)
	next = request.GET.get('next', settings.HOME_URL)
	if request.method == 'POST':
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)
			messages.success(request, "Password has been successfully updated!")
			return redirect(next)
		else:
			messages.error(request, "Password has not been successfully updated. Try again!")
	contex = {
		'form': form,
		'next': next
	}
	return render(request, 'auth/change_password.html', contex)

def user_index(request):
	users = User.objects.all()
	contex = {
		'users': users,
		'title': 'User'
	}
	return render(request, 'user/index.html', contex)

def user_profile(request):
	user = User.objects.get(pk = request.user.id)
	if request.method == 'POST':
		old_image = user.profile_image
		profile_image_form = ProfileImageForm(request.POST, request.FILES, instance = user)
		if profile_image_form.is_valid():
			user = profile_image_form.save()
			if old_image:
				os.remove(old_image.path)
			messages.success(request, "Profile image has been successfully updated")
			return redirect('Auth:user_profile')
		else:
			messages.success(request, "Problem in uploading image.Try again")

	profile_image_form = ProfileImageForm()
	return render(request, 'user/profile.html', {'user': user, 'profile_image_form': profile_image_form})

def user_save(request, id = None):
	if id:
		instance = User.objects.get(pk = get_decoded_id(id))
		instance.password = ""
		form = UserUpdateForm(request.POST or None, instance = instance)
	else:
		form = UserRegisterForm(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			user = form.save()
			if id:
				user.updated_by = request.user
			else:
				user.created_by = request.user
			user.save()
			messages.success(request, "User has been successfully "+ ("updated" if id else "added") +"!")
			return redirect('Auth:user_index')
		else:
			messages.error(request, "User has not been successfully "+ ("updated" if id else "added") +"!")

	contex = {
		'form': form,
		'title': 'Update User' if id else 'Add User'
	}
	return render(request, 'user/save.html', contex)


def user_delete(request, id):
	user = User.objects.get(pk = get_decoded_id(id))
	user.delete()
	messages.success(request, "User has been successfully deleted!")
	return redirect('Auth:user_index')
