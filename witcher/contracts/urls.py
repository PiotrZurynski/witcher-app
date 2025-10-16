from django.urls import path, include 
from . import views
from .views import ContractCreateForm

urlpatterns = [
    path("",views.home,name="home"),
    path("login/",views.login_view,name="login"),
    path("logout/",views.logout_view,name="logout"),
    path("signup/",views.SignUp.as_view(),name="signup"),
    path('contracts/create',views.ContractCreate.as_view(),name="contractcreate"),
    path('contract/list', views.ContractList.as_view(),name="contractlist"),
]