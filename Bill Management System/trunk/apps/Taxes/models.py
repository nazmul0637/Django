from django.db import models
from datetime import datetime
from django.conf import settings
from Auth.models import User
from django.utils.translation import ugettext_lazy as _


# Create your models here.

class Tax(models.Model):
	tax_type=models.CharField(_('tax type'), choices=(('V', 'VAT'), ('T', 'Tax')), max_length=1)
	name=models.CharField(_('name'), max_length=40)
	percentage=models.DecimalField(_('percentage'), max_digits=5, decimal_places=2)
	created_at = models.DateTimeField(default = datetime.now)
	updated_at = models.DateTimeField(auto_now = True)
	created_by = models.ForeignKey(User)
	updated_by = models.ForeignKey(User, null = True)

	def __str__(self):
		return self.name

	def get_encoded_id(self):
		return settings.HASHID.encode(self.id)

	class Meta:
		db_table = 'taxes'