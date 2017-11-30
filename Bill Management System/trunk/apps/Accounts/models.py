from django.db import models
from django.conf import settings
from datetime import datetime
from Auth.models import User
from Invoicing.models import Invoice, ContractAgreementPurpose
from Portfolio.models import Product
from django.core.validators import MinValueValidator
from django.db.models import Sum

# Create your models here.

class ExpensePurpose(models.Model):
	name = models.CharField(max_length = 100)
	code = models.PositiveIntegerField(unique = True)
	description = models.TextField(null = True)
	created_at = models.DateTimeField(default = datetime.now)
	updated_at = models.DateTimeField(auto_now = True)
	created_by = models.ForeignKey(User, related_name = "expense_purpose_created_by")
	updated_by = models.ForeignKey(User, null = True, related_name = "expense_purpose_updated_by")

	def __str__(self):
		return self.name

	def get_encoded_id(self):
		return settings.HASHID.encode(self.id)

	class Meta:
		db_table = 'expense_purposes'

class Expenditure(models.Model):
	product = models.ForeignKey(Product, on_delete = models.CASCADE, related_name = 'expenditures')
	exp_id = models.CharField(max_length = 20)
	seq_num = models.PositiveIntegerField()
	date = models.DateField()
	description = models.TextField(null = True)
	created_at = models.DateTimeField(default = datetime.now)
	updated_at = models.DateTimeField(auto_now = True)
	created_by = models.ForeignKey(User, related_name = "expenditure_created_by")
	updated_by = models.ForeignKey(User, null = True, related_name = "expenditure_updated_by")

	def get_encoded_id(self):
		return settings.HASHID.encode(self.id)

	def get_total_expense(self):
		total_expense = self.expenditure_details.aggregate(Sum('amount'))
		return total_expense['amount__sum']

	def get_date(self):
		return self.date.strftime('%Y-%m-%d')

	class Meta:
		db_table = 'expenditures'

class ExpenditureDetail(models.Model):
	expenditure = models.ForeignKey(Expenditure, on_delete = models.CASCADE, related_name = 'expenditure_details')
	expense_purpose = models.ForeignKey(ExpensePurpose, on_delete = models.CASCADE, related_name = 'expenses')
	amount = models.FloatField()

	def get_encoded_id(self):
		return settings.HASHID.encode(self.id)

	class Meta:
		db_table = 'expenditure_details'


class Collection(models.Model):
	invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="collections")
	collected_amount = models.FloatField(validators=[MinValueValidator(0.0)])
	description = models.TextField(null=True)
	collection_date = models.DateField(auto_now=False,auto_now_add=False)
	collected_by = models.ForeignKey(User, related_name = "collection_collected_by")
	created_at = models.DateTimeField(default = datetime.now)
	updated_at = models.DateTimeField(auto_now = True)
	created_by = models.ForeignKey(User, related_name = "collection_created_by")
	updated_by = models.ForeignKey(User, null = True, related_name = "collection_updated_by")

	def get_encoded_id(self):
		return settings.HASHID.encode(self.id)

	class Meta:
		db_table = 'collections'

class CollectionDetail(models.Model):
	collection = models.ForeignKey(Collection, on_delete = models.CASCADE, related_name = 'collection_details')
	contract_agreement_purpose = models.ForeignKey(ContractAgreementPurpose, on_delete = models.CASCADE)
	collected_amount = models.FloatField(validators=[MinValueValidator(0.0)])

	def get_encoded_id(self):
		return settings.HASHID.encode(self.id)	
	
	class Meta:
		db_table = 'collection_details'
