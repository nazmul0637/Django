from django.db import models
from datetime import datetime
from django.conf import settings
from Auth.models import User

# Create your models here.
class Manager(models.Manager):
	def active(self):
		return self.filter(status = True)

class Client(models.Model):
	name = models.CharField(max_length=40)
	short_name = models.CharField(max_length = 10)
	code = models.PositiveIntegerField()
	address= models.CharField(max_length=100)
	contact_number = models.CharField(max_length=20)
	email = models.EmailField(unique = True)
	description = models.TextField(null = True)
	status = models.BooleanField()
	created_at = models.DateTimeField(default = datetime.now)
	updated_at = models.DateTimeField(auto_now = True)
	created_by = models.ForeignKey(User, related_name = "client_created_by")
	updated_by = models.ForeignKey(User, null = True, related_name = "client_updated_by")
	objects = Manager()

	def __str__(self):
		return self.name+"("+self.short_name+")"

	def get_short_name(self):
		return self.short_name

	def get_encoded_id(self):
		return settings.HASHID.encode(self.id)

	def get_description(self):
		return self.description or 'Not Available'

	def get_info(self):
		return self.name+'\n'+self.address

	def get_email(self):
		if self.email:
			return self.email
		return "Not Available"

	def get_status(self):
		if self.status:
			return "Active"
		return "Closed"

	class Meta:
		db_table = 'clients'
			
class ConcernPerson(models.Model):
	name = models.CharField(max_length=40)
	designation = models.CharField(max_length=50)
	division = models.CharField(max_length=40)
	contact_number = models.CharField(max_length = 20)
	email = models.EmailField(null = True)
	client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name = 'concern_persons')
	status = models.BooleanField()
	objects = Manager()
	def __str__(self):
		return self.name+'('+self.designation+')'

	def get_encoded_id(self):
		return settings.HASHID.encode(self.id)

	def get_email(self):
		return self.email or 'Not Available'

	def get_status(self):
		if self.status:
			return "Active"
		return "Closed"

	class Meta:
		db_table = 'client_concern_persons'