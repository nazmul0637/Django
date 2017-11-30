from django.conf import settings

def global_settings(request):
	return {
		'HOME_URL': settings.HOME_URL,
		'LOGIN_URL': settings.LOGIN_URL,
		'LOGOUT_URL': settings.LOGOUT_URL,
		'CHANGE_PASSWORD_URL': settings.CHANGE_PASSWORD_URL,
		'HASHID': settings.HASHID,
	}