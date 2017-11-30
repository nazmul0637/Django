from django.conf import settings
from datetime import datetime
from dateutil.relativedelta import relativedelta
from Settings.models import Holiday
ordinal_suffix={1:'st', 2: 'nd', 3: 'rd'}

def get_encoded_id(id):
	return settings.HASHID.encode(id)

def get_decoded_id(encoded_id):
	return settings.HASHID.decode(encoded_id)[0]

def get_ordinal(num):
	return str(num)+(ordinal_suffix[num%10] if num%10 in ordinal_suffix.keys() else "th")

def get_work_day(date):
	holiday = Holiday.objects.filter(holiday_date = date)
	while holiday:
		date = date + relativedelta(days = 1)
		holiday = Holiday.objects.filter(holiday_date = date)
	return date