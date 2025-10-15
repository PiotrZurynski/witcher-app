from django.shortcuts import render
from django.http import HttpResponse
from .models import Contract
from django.views.generic.edit import CreateView
from .forms import ContractCreateForm
# Create your views here.
def home(request):
    return render(request,"contracts/home.html")


class ContractCreate(CreateView):
    model=Contract
    template_name='contracts/contract_create_form.html'
    form_class=ContractCreateForm