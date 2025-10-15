from django.urls import path, include 
from . import views
from .views import ContractCreateForm

urlpatterns = [
    path("",views.home,name="home"),
    path('contracts/create',views.ContractCreate.as_view(),name="contractcreate")
]