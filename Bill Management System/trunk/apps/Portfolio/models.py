from django.conf import settings
from django.db import models
from datetime import datetime
from Auth.models import User
from Employees.models import Employee

# Create your models here.

class Manager(models.Manager):
	def active(self):
		return self.filter(status = True)

class Portfolio(models.Model):
	concern_persons = models.ManyToManyField(Employee)
	name = models.CharField(max_length = 40)
	start_date = models.DateField()
	end_date = models.DateField(null = True)
	description = models.TextField(null = True)
	status = models.BooleanField(default = True)
	created_at = models.DateTimeField(default = datetime.now)
	updated_at = models.DateTimeField(auto_now = True)
	created_by = models.ForeignKey(User, related_name = "portfolio_created_by")
	updated_by = models.ForeignKey(User, null = True, related_name = "portfolio_updated_by")
	objects = Manager()

	def __str__(self):
		return self.name

	def get_encoded_id(self):
		return settings.HASHID.encode(self.id)

	def get_status(self):
		if self.status:
			return "Active"
		return "Closed"

	class Meta:
		db_table = 'portfolios'

class Purpose(models.Model):
	name = models.CharField(max_length = 40, unique = True)
	description = models.TextField(null = True)
	status = models.BooleanField(default = True)
	created_at = models.DateTimeField(default = datetime.now)
	updated_at = models.DateTimeField(auto_now = True)
	created_by = models.ForeignKey(User, related_name = "purpose_created_by")
	updated_by = models.ForeignKey(User, null = True, related_name = "purpose_updated_by")
	objects = Manager()

	def __str__(self):
		return self.name

	def get_encoded_id(self):
		return settings.HASHID.encode(self.id)

	def get_status(self):
		if self.status:
			return "Active"
		return "Disable"

	class Meta:
		db_table = 'purposes'

class Product(models.Model):
	concern_persons = models.ManyToManyField(Employee, through = 'ProductConcernPerson')
	portfolio = models.ForeignKey(Portfolio, on_delete = models.CASCADE, related_name = 'products')
	name = models.CharField(max_length = 40)
	short_name = models.CharField(max_length = 10, unique = True)
	product_type=models.CharField(choices=(('Project', 'Project'), ('Product', 'Product')), max_length=7)
	description = models.TextField(null = True)
	status = models.BooleanField(default = True)
	purposes = models.ManyToManyField(Purpose, through = 'ProductPurpose')
	start_date = models.DateField()
	end_date = models.DateField(null = True)
	created_at = models.DateTimeField(default = datetime.now)
	updated_at = models.DateTimeField(auto_now = True)
	created_by = models.ForeignKey(User, related_name = "product_created_by")
	updated_by = models.ForeignKey(User, null = True, related_name = "product_updated_by")
	objects = Manager()

	def __str__(self):
		return self.name+"("+self.short_name+")"

	def get_short_name(self):
		return self.short_name

	def get_encoded_id(self):
		return settings.HASHID.encode(self.id)

	def get_status(self):
		if self.status:
			return "Active"
		return "Closed"

	def get_concern_persons(self):
		concern_persons = ',\n'.join([concern_person.__str__() for concern_person in self.concern_persons.all()])
		return concern_persons

	class Meta:
		db_table = 'products'

class ProductConcernPerson(models.Model):
	product = models.ForeignKey(Product, on_delete = models.CASCADE)
	employee = models.ForeignKey(Employee, on_delete = models.CASCADE)

	class Meta:
		db_table = 'product_concern_persons'

class ProductPurpose(models.Model):
	product = models.ForeignKey(Product, on_delete = models.CASCADE)
	purpose = models.ForeignKey(Purpose, on_delete = models.CASCADE)
	amount = models.FloatField(default = 0)

	class Meta:
		db_table = 'product_purposes'