from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Contract
from django.views.generic.edit import CreateView
from .forms import ContractCreateForm
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
# Create your views here.
def home(request):
    return render(request,"contracts/home.html")

def login_view(request):
    context={
        "login_view":"active"
    }
    if request.method == "POST":
        login=request.POST("login")
        password=request.POST("password")

        user=authenticate(request,login=login,password=password)

        if user is not None:
            login(request, user)
            return redirect("home.html")
        else:
            return HttpResponse("Złe dane")
    return render(request, "contracts/login.html", context)
class ContractCreate(CreateView):
    model=Contract
    template_name='contracts/contract_create_form.html'
    form_class=ContractCreateForm
    success_url=reverse_lazy('home')
