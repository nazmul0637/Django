from django.db import models
from datetime import datetime
from django.conf import settings
from BMS.utils import get_ordinal
from Auth.models import User
from Portfolio.models import Product, Purpose
from Clients.models import Client, ConcernPerson
from Settings.models import Bankaccount, Invoicetemplate
from django.core.validators import MinValueValidator

# Create your models here.
class Manager(models.Manager):
	def active(self):
		return self.filter(status = True)	
	# def due_or_paid_invoice(self):
	# 	return self.filter(status = 2 or 3)

class ContractAgreement(models.Model):
	client = models.ForeignKey(Client, on_delete = models.CASCADE, related_name = 'contract_agreement')
	product = models.ForeignKey(Product, on_delete = models.CASCADE, related_name = 'contract_agreement')
	agreement_date = models.DateField()
	end_date = models.DateField(null = True)
	net_amount = models.FloatField(validators = [MinValueValidator(1.0)])
	mode_of_payment = models.CharField(max_length = 5)
	bank_account = models.ForeignKey(Bankaccount, null = True, on_delete = models.CASCADE)
	invoice_template = models.ForeignKey(Invoicetemplate, on_delete = models.CASCADE)
	vat = models.FloatField(null = True, validators = [MinValueValidator(0.0)])
	status = models.BooleanField(default = True)
	created_at = models.DateTimeField(default = datetime.now)
	updated_at = models.DateTimeField(auto_now = True)
	created_by = models.ForeignKey(User, related_name = "contract_agreement_created_by")
	updated_by = models.ForeignKey(User, null = True, related_name = "contract_agreement_updated_by")
	objects = Manager()

	def get_encoded_id(self):
		return settings.HASHID.encode(self.id)

	def get_status(self):
		if self.status:
			return "Active"
		return "Closed"

	def get_agreement_date(self):
		return self.agreement_date.strftime('%Y-%m-%d')

	def get_vat(self):
		if self.vat:
			return str(self.vat)+'%'
		return "Not Applicable"

	def get_concern_persons(self):
		concern_persons = ',\n'.join([concern_person.concern_person.__str__() for concern_person in self.concern_persons.all()])
		return concern_persons
	class Meta:
		db_table = 'contract_agreement'

class ContractAgreementConcernPerson(models.Model):
	contract_agreement = models.ForeignKey(ContractAgreement, on_delete = models.CASCADE, related_name = 'concern_persons')
	concern_person_type = models.CharField(max_length = 8)
	concern_person = models.ForeignKey(ConcernPerson, on_delete = models.CASCADE)

	class Meta:
		db_table = 'contract_agreement_concern_persons'

class ContractAgreementPurpose(models.Model):
	contract_agreement = models.ForeignKey(ContractAgreement, on_delete = models.CASCADE, related_name = 'purposes')
	purpose = models.ForeignKey(Purpose, on_delete = models.CASCADE)
	amount_per_installment = models.FloatField(validators = [MinValueValidator(1.0)], null = True)
	amount = models.FloatField(validators = [MinValueValidator(1.0)])
	num_installment = models.IntegerField(validators = [MinValueValidator(1)])

	def __str__(self):
		return self.purpose.name

	def get_per_installment_amount(self):
		return self.amount_per_installment if self.amount_per_installment else ""

	class Meta:
		db_table = 'contract_agreement_purposes'

invoice_status = {'0': 'Draft', '1': 'Submitted', '2': 'Due', '3': 'Paid'}
class Invoice(models.Model):
	contract_agreement = models.ForeignKey(ContractAgreement, on_delete = models.CASCADE, related_name = 'invoices')
	invoice_sequence = models.PositiveIntegerField()
	invoice_no = models.CharField(max_length = 20, null = True)
	amount=models.FloatField(default=0)
	subject = models.TextField()
	date = models.DateField()
	status = models.PositiveIntegerField(default = 0)
	created_at = models.DateTimeField(default = datetime.now)
	updated_at = models.DateTimeField(auto_now = True)
	created_by = models.ForeignKey(User, related_name = "invoice_created_by")
	updated_by = models.ForeignKey(User, null = True, related_name = "invoice_updated_by")
	objects=Manager()

	def __str__(self):
		return 'Invoice No:'+self.invoice_no+' '+'Client:'+self.contract_agreement.client.__str__()

	def get_invoice_no(self):
		return self.invoice_no

	def get_encoded_id(self):
		return settings.HASHID.encode(self.id)

	def get_status(self):
		return invoice_status[str(self.status)]

	def get_date(self):
		return self.date.strftime('%Y-%m-%d')

	class Meta:
		db_table = 'invoices'

class BillInstallmentConfig(models.Model):
	contract_agreement_purpose = models.OneToOneField(ContractAgreementPurpose, on_delete = models.CASCADE, related_name = 'bill_installment_config')
	installment_type = models.IntegerField()
	particular = models.TextField()
	use_sequence = models.BooleanField(default = False)
	schedule_start_date = models.DateField()

	class Meta:
		db_table = 'bill_installment_configs'

class BillSchedule(models.Model):
	installment_num = models.IntegerField()
	contract_agreement_purpose = models.ForeignKey(ContractAgreementPurpose, related_name = 'bill_schedules')
	particular = models.TextField()
	schedule_date = models.DateField()
	amount = models.FloatField(validators = [MinValueValidator(1.0)])
	invoice = models.ForeignKey(Invoice, null = True, related_name = "bill_schedules")
	bill_installment_config = models.ForeignKey(BillInstallmentConfig, null = True, on_delete = models.CASCADE, related_name = 'bill_schedules')

	def get_installment_num(self):
		return get_ordinal(self.installment_num)
	class Meta:
		db_table = 'bill_schedules'





