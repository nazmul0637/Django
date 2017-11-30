from django.shortcuts import render, redirect, get_object_or_404
from .models import Tax
from .forms import TaxForm
from django.contrib import messages
from BMS.utils import get_decoded_id


# Create your views here.


def tax_index(request):
	taxes = Tax.objects.all()
	contex = {
		'taxes': taxes,
		'title': 'Tax' 
	}
	return render(request, 'tax/index.html', contex)

def tax_detail(request, id):
	tax = get_object_or_404(Tax, pk = get_decoded_id(id))
	return render(request, 'tax/detail.html', {'tax': tax})

def tax_save(request, id = None):
	instance = get_object_or_404(Tax, pk = get_decoded_id(id)) if id else None
	form=TaxForm(request.POST or None, instance = instance)
	#next = request.GET.get('next')
	if request.method == 'POST':
		if form.is_valid():
			instance=form.save(commit=False)
			if id:
				instance.updated_by = request.user.id
			else:
				instance.created_by = request.user.id
			instance.save()
			messages.success(request, "Employee has been successfully "+ ("updated" if id else "added") +"!")
			return redirect('Taxes:tax_detail', instance.get_encoded_id())
	
	contex={
		"form":form,
		'title': 'Update Employee' if id else 'Add Employee',
		#'next': next
	}
	return render(request,"tax/save.html",contex)

def tax_delete(request, id):
	tax = get_object_or_404(Tax, pk = get_decoded_id(id))
	tax.delete()
	messages.success(request, "Employee has been successfully deleted!")
	return redirect('Taxes:tax_index')