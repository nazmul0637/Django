from django.db import models
from datetime import datetime
from django.conf import settings
from Auth.models import User

# Create your models here.

class Invoicetemplate(models.Model):
	title = models.CharField(max_length=40, unique = True)
	template_body =models.TextField()
	status = models.BooleanField()
	created_at = models.DateTimeField(default = datetime.now)
	updated_at = models.DateTimeField(auto_now = True)
	created_by = models.ForeignKey(User, related_name = "invoice_template_created_by")
	updated_by = models.ForeignKey(User, null = True, related_name = "invoice_template_updated_by")

	class Meta:
		db_table = 'custom_invoice_templates'

	def __str__(self):
		return self.title

	def get_encoded_id(self):
		return settings.HASHID.encode(self.id)

	def get_status(self):
		if self.status:
			return "Active"
		return "Not Active"

	def get_template_body(self):
		return self.template_body if self.template_body else "Not available"

class Bankaccount(models.Model):
	name_of_account = models.CharField(max_length=40)
	account_no = models.CharField(max_length=20, unique = True)
	bank_name = models.CharField(max_length=40)
	branch_name = models.CharField(max_length=40)
	address = models.CharField(max_length=100)
	swift_code = models.CharField(max_length=50)
	routing_no =models.CharField(max_length=20)
	created_at = models.DateTimeField(default = datetime.now)
	updated_at = models.DateTimeField(auto_now = True)
	created_by = models.ForeignKey(User, related_name = "bankaccount_created_by")
	updated_by = models.ForeignKey(User, null = True, related_name = "bankaccount_updated_by")

	class Meta:
		db_table = 'account_details'

	def __str__(self):
		return self.name_of_account+'('+self.account_no+')'

	def get_encoded_id(self):
		return settings.HASHID.encode(self.id)

class Holiday(models.Model):
	branch_id = models.PositiveIntegerField(null = True, default = None)
	holiday_date = models.DateField(auto_now=False,auto_now_add=False)
	holiday_type = models.CharField(max_length=7)
	description = models.TextField(null=True)
	created_at = models.DateTimeField(default = datetime.now)
	updated_at = models.DateTimeField(auto_now = True)
	created_by = models.ForeignKey(User, related_name = "holiday_created_by")
	updated_by = models.ForeignKey(User, null = True, related_name = "holiday_updated_by")

	class Meta:
		db_table = 'holidays'

	def __str__(self):
		return str(self.holiday_date)

	def get_encoded_id(self):
		return settings.HASHID.encode(self.id)

	def get_holiday_type(self):
		if self.holiday_type == "Weekly":
			return "Weekly"
		if self.holiday_type == "Holiday":
			return "Holiday"
		return "Others"

	def get_description(self):
		return self.description if self.description else "Not available"
