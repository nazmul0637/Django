from django.shortcuts import redirect
from django.conf import settings
def anonymous_required(redirect_url = None):
	def wrap_view(function):
		def wrap(request, *args, **kwargs):
			if request.user.is_authenticated:
				return redirect(redirect_url or settings.HOME_URL)
			return function(request, *args, **kwargs)
		return wrap
	return wrap_view