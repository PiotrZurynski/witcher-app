from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Contract
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from .forms import ContractCreateForm
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
# Create your views here.
def home(request):
    context={"name": request.user}
    return render(request,"contracts/home.html",context)

def login_view(request):
    context={
        "login_view":"active"
    }
    if request.method == "POST":
        username=request.POST.get("username")
        password=request.POST.get("password")

        user=authenticate(request,username=username,password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return HttpResponse("Złe dane")
    return render(request, "registration/login.html", context)
def logout_view(request):
    logout(request)
    return redirect("home")

class SignUp(CreateView):
    form_class=UserCreationForm
    success_url=reverse_lazy("login")
    template_name="registration/signup.html"
class ContractCreate(LoginRequiredMixin,CreateView):
    model=Contract
    template_name='contracts/contract_create_form.html'
    form_class=ContractCreateForm
    success_url=reverse_lazy('home')
    login_url=reverse_lazy('login')

class ContractList(ListView):
    model=Contract