from BMS.utils import get_decoded_id
from django.shortcuts import render, redirect, get_object_or_404
from .models import Portfolio, Product, Purpose, ProductPurpose, ProductConcernPerson
from .forms import PortfolioCreationForm, ProductCreationForm, PurposeCreationForm
from django.http import HttpResponse
from django.contrib import messages
from datetime import datetime
import json
# save your views here.

def portfolio_index(request):
	portfolios = Portfolio.objects.all()
	contex = {
		'portfolios': portfolios,
		'title': 'Portfolio'
	}
	return render(request, 'portfolio/index.html', contex)

def portfolio_detail(request, id):
	portfolio = get_object_or_404(Portfolio, pk = id)
	return render(request, 'portfolio/detail.html', {'portfolio': portfolio})

def portfolio_save(request, id = None):
	portfolio = None if id == None else Portfolio.objects.get(pk = id)
	form = PortfolioCreationForm(request.POST or None, instance = portfolio)
	if request.method == 'POST':
		if form.is_valid():
			portfolio = form.save(commit = False)
			if id:
				portfolio.updated_by = request.user
			else:
				portfolio.created_by = request.user
			if portfolio.status:
				portfolio.end_date = None
			else:
				portfolio.end_date = datetime.now()

			portfolio.save()
			form.save_m2m()
			messages.success(request, "Portfolio has been successfully "+ ("created" if id==None else "updated"))
		else:
			messages.error(request, "Portfolio has not been successfully "+ ("created" if id==None else "updated"))
	contex = {
		'form': form,
		'title': 'Portfolio'
	}
	return render(request, 'modal_form/save.html', contex)

def portfolio_delete(request, id):
	portfolio = Portfolio.objects.get(pk = get_decoded_id(id))
	portfolio.delete()
	messages.success(request, "Portfolio has been successfully deleted")
	return redirect('Portfolio:portfolio_index')

def product_list(request, portfolio_id):
	if request.is_ajax():
		products = Product.objects.filter(portfolio = Portfolio.objects.get(pk = portfolio_id))
		data = {}
		for product in products:
			data[product.id] = product.name
		return HttpResponse(json.dumps(data), content_type = 'application/json')


def product_index(request):
	products = Product.objects.all()
	contex = {
		'products': products,
		'title': 'Product'
	}
	return render(request, 'product/index.html', contex)

def product_detail(request, id):
	product = get_object_or_404(Product, pk = id)
	return render(request, 'product/detail.html', {'product': product})

def product_save(request, id = None):
	product = None if id == None else Product.objects.get(pk = get_decoded_id(id))
	form = ProductCreationForm(request.POST or None, instance = product)
	if request.method == 'POST':
		if form.is_valid():
			product = form.save(commit = False)
			if id:
				product.updated_by = request.user
			else:
				product.created_by = request.user
			if product.status:
				product.end_date = None
			else:
				product.end_date = datetime.now()

			product.save()
			concern_persons = form.cleaned_data.get('concern_persons')
			for concern_person in concern_persons:
				product_concern_person, created = ProductConcernPerson.objects.get_or_create(product = product, employee = concern_person)
				product_concern_person.save()
			ProductConcernPerson.objects.filter(product = product).exclude(employee__in = concern_persons).delete()

			purposes = form.cleaned_data.get('purposes')
			for purpose in purposes:
				amount = request.POST.get('purpose_'+str(purpose.id))
				product_purpose, created = ProductPurpose.objects.get_or_create(product = product, purpose = purpose)
				product_purpose.amount = amount
				product_purpose.save()
			ProductPurpose.objects.filter(product = product).exclude(purpose__in = purposes).delete()

			messages.success(request, "Product has been successfully "+ ("created" if id==None else "updated"))
			return redirect('Portfolio:product_index')
		else:
			messages.error(request, "Product has not been successfully "+ ("created" if id==None else "updated"))

	contex = {
		'form': form,
		'title': 'Add Product' if id==None else 'Update Product'
	}
	return render(request, 'product/save.html', contex)

def product_delete(request, id):
	product = Product.objects.get(pk = get_decoded_id(id))
	product.delete()
	messages.success(request, "Product has been successfully deleted")
	return redirect('Portfolio:product_index')

def purpose_list(request, product_id):
	if request.is_ajax():
		purposes = Purpose.objects.filter(product = Product.objects.get(pk = product_id))
		data = {}
		for purpose in purposes:
			data[purpose.id] = purpose.name
		return HttpResponse(json.dumps(data), content_type = 'application/json')

def purpose_index(request):
	purposes = Purpose.objects.all()
	contex = {
		'purposes': purposes,
		'title': 'Purpose'
	}
	return render(request, 'purpose/index.html', contex)

def purpose_save(request, id = None):
	purpose = None if id == None else Purpose.objects.get(pk = id)
	form =  PurposeCreationForm(request.POST or None, instance = purpose)
	if request.method == 'POST':
		if form.is_valid():
			purpose = form.save(commit = False)
			if id:
				purpose.updated_by = request.user
			else:
				purpose.created_by = request.user
			purpose.save()
			messages.success(request, "Purpose has been successfully "+ ("created" if id==None else "updated"))
		else:
			messages.error(request, "Purpose has not been successfully "+ ("created" if id==None else "updated"))

	contex = {
		'form': form,
		'title': 'Purpose'
	}
	return render(request, 'modal_form/save.html', contex)

def purpose_delete(request, id):
	purpose = Purpose.objects.get(pk = get_decoded_id(id))
	purpose.delete()
	messages.success(request, "Purpose has been successfully deleted")
	return redirect('Portfolio:purpose_index')
