from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Contract, Realm
from django.views.generic import ListView, UpdateView, DeleteView, DetailView
from django.views.generic.edit import CreateView
from .forms import ContractCreateForm
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
# Create your views here.
def home(request):
    realms=['Temeria','Redania','Skellige','Nilfgaard']
    realm_id=Realm.objects.filter(name__in=realms)

    context={'realms':realm_id,"name": request.user}
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

class OwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        obj=self.get_object()
        return obj.owner_id==self.request.user.id

    def handle_no_permission(self):
        return super().handle_no_permission()

class ContractList(ListView):
    model=Contract

    def get_queryset(self):
        queryset=super().get_queryset()
        sort=self.request.GET.get('sort','newest')

        if sort=='newest':
            queryset=queryset.order_by('-time_created')
        elif sort=='reward':
            queryset=queryset.order_by('-reward')
        elif sort=='realm':
            queryset =queryset.order_by('realm__name')
        return queryset


class ContractCreate(LoginRequiredMixin,CreateView):
    model=Contract
    template_name='contracts/contract_create_form.html'
    form_class=ContractCreateForm
    success_url=reverse_lazy('profile')

    def form_valid(self, form):
        form.instance.owner=self.request.user
        return super().form_valid(form)

class ContractUpdate(LoginRequiredMixin,OwnerRequiredMixin,UpdateView):
    model=Contract
    form_class=ContractCreateForm
    template_name="contracts/contract_create_form.html"
    success_url=reverse_lazy('profile')

    def form_valid(self,form):
        return super().form_valid(form)
    
class ContractDelete(LoginRequiredMixin,OwnerRequiredMixin,DeleteView):
    model=Contract
    template_name="contracts/contract_confirm_delete.html"
    success_url=reverse_lazy('profile')

    
class ProfileView(LoginRequiredMixin,ListView):
    model=Contract
    template_name="contracts/profile.html"
    context_object_name="contracts"
    paginate_by=10

    def get_queryset(self):
        return (Contract.objects.filter(owner=self.request.user).select_related("realm", "town", "monster").order_by("-time_created"))    


    
class ContractDetailView(DetailView):
    model=Contract
    template_name='contracts/contract_detail.html'
    context_object_name='contract'