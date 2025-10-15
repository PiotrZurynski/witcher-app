from django.shortcuts import render
from django.http import HttpResponse
from .models import Contract
from django.views.generic.edit import CreateView
from .forms import ContractCreateForm
from django.urls import reverse_lazy
# Create your views here.
def home(request):
    return render(request,"contracts/home.html")


class ContractCreate(CreateView):
    model=Contract
    template_name='contracts/contract_create_form.html'
    form_class=ContractCreateForm
    success_url=reverse_lazy('home')