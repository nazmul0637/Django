from django.db import models
from datetime import datetime
from django.conf import settings
from django.core.validators import MinValueValidator
from Auth.models import User

#Create your models here.

class Manager(models.Manager):
	def active(self):
		return self.filter(status = True)

class Designation(models.Model):
	title = models.CharField(max_length=40)
	status = models.BooleanField()
	created_by = models.ForeignKey(User, related_name = "designation_created_by")
	updated_by = models.ForeignKey(User, null = True, related_name = "designation_updated_by")
	objects = Manager()

	def __str__(self):
		return self.title

	def get_encoded_id(self):
		return settings.HASHID.encode(self.id)

	def get_status(self):
		if self.status:
			return "Active"
		return "Disable"

	class Meta:
		db_table = 'designations'

def upload_location(instance, filename):
	return '/'.join(['images', 'employees', instance.employee_id, filename])

class Employee(models.Model):
	name = models.CharField(max_length=40)
	employee_id = models.CharField(max_length = 20, unique = True)
	designation = models.ForeignKey(Designation, on_delete=models.CASCADE)
	father_name = models.CharField(max_length=40)
	mother_name = models.CharField(max_length=40)
	present_address= models.CharField(max_length=100)
	permanent_address =models.CharField(max_length=100)
	gender = models.CharField(max_length=6)
	date_of_birth = models.DateField(auto_now = False, auto_now_add = False)
	contact_number = models.CharField(max_length=20)
	email = models.EmailField(unique = True)
	date_of_joining = models.DateField(auto_now=False,auto_now_add=False)
	starting_salary = models.FloatField(null = True, validators = [MinValueValidator(1.0)])
	current_salary = models.FloatField(null = True, validators = [MinValueValidator(1.0)])
	national_id = models.CharField(max_length=20, null = True)
	profile_image = models.ImageField(upload_to = upload_location, null = True)
	status = models.BooleanField()
	created_at = models.DateTimeField(default = datetime.now)
	updated_at = models.DateTimeField(auto_now = True)
	created_by = models.ForeignKey(User, related_name = "employee_created_by")
	updated_by = models.ForeignKey(User, null = True, related_name = "employee_updated_by")
	objects = Manager()

	class Meta:
		db_table = 'employees'

	def __str__(self):
		return self.name+' ('+self.employee_id+')'

	def get_encoded_id(self):
		return settings.HASHID.encode(self.id)

	def get_gender(self):
		if self.gender == "M":
			return "Male"
		if self.gender == "F":
			return "Female"
		return "Others"

	def get_starting_salary(self):
		return self.starting_salary if self.starting_salary else "Not available"

	def get_current_salary(self):
		return self.current_salary if self.current_salary else "Not available"

	def get_national_id(self):
		return self.national_id if self.national_id else "Not available"

	def get_status(self):
		if self.status:
			return "Active"
		return "Not Active"

	def get_profile_image(self):
		if self.profile_image:
			return self.profile_image.url
		if self.gender == 'F':
			return '/media'+'/'+'images/employees/profile-default-female.jpg'
		else:
			return '/media'+'/'+'images/employees/profile-default-male.png'