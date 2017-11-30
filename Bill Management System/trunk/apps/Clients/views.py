from django.shortcuts import render, redirect, get_object_or_404
from django.forms.formsets import formset_factory
from django.db import IntegrityError, transaction
from django.http import HttpResponse
from .forms import ClientForm, ConcernPersonForm, ConcernPersonFormSet
from .models import Client, ConcernPerson
from django.contrib import messages
from BMS.utils import get_decoded_id
import json

# Create your views here.

def client_index(request):
	clients = Client.objects.all()
	contex = {
		'clients': clients,
		'title': 'Client'
	}
	return render(request, 'client/index.html', contex)

def client_detail(request, id):
	client = get_object_or_404(Client, pk = id)
	return render(request, 'client/detail.html', {'client': client})

def client_save(request, id = None):
	client = get_object_or_404(Client, pk = get_decoded_id(id)) if id else None
	client_form=ClientForm(request.POST or None, instance = client)
	concern_person_formset = ConcernPersonFormSet(instance = client)
	if request.method == 'POST':
		if client_form.is_valid():
			client = client_form.save(commit = False)
			if id:
				client.updated_by = request.user
			else:
				client.created_by = request.user

			concern_person_formset = ConcernPersonFormSet(request.POST, instance = client)
			if concern_person_formset.is_valid():
				client.save()
				concern_person_formset.save()
				messages.success(request, "Client has been successfully "+ ("created" if id==None else "updated"))
				return redirect('Clients:client_index')
				
		messages.error(request, "Client Information has not been successfully "+ ("created" if id==None else "updated"))
		
	contex={
		"client_form":client_form,
		'concern_person_formset': concern_person_formset,
		'title': 'Update Client' if id else 'Add Client Information'
	}
	return render(request,"client/save.html",contex)

def client_delete(request, id):
	client = get_object_or_404(Client, pk = get_decoded_id(id))
	client.delete()
	messages.success(request, "Client has been successfully deleted!")
	return redirect('Clients:client_index')


def concern_person_list(request, client_id):
	concern_persons = ConcernPerson.objects.filter(client = Client.objects.get(pk = client_id))
	data = {}
	for concern_person in concern_persons:
		data[concern_person.id] = concern_person.__str__()
	return HttpResponse(json.dumps(data), content_type = 'application/json')