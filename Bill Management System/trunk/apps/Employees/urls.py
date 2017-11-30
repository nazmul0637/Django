from django.conf.urls import url
from .views import *

app_name='Employees'
urlpatterns = [
url(r'^index/$', employee_index, name = 'employee_index'),
url(r'^save/$', employee_save, name ='employee_save'),
url(r'^save/(?P<id>[\w]+)/$', employee_save, name = 'employee_save'),
url(r'^detail/(?P<id>[\w]+)/$', employee_detail, name = 'employee_detail'),
url(r'^delete/(?P<id>[\w]+)/$', employee_delete, name = 'employee_delete'),
url(r'^designation/index/$', designation_index, name = 'designation_index'),
url(r'^designation/save/$', designation_save, name = 'designation_save'),
url(r'^designation/save/(?P<id>[\w]+)$', designation_save, name = 'designation_save'),
url(r'^designation/delete/(?P<id>[\w]+)$', designation_delete, name = 'designation_delete'),

]
