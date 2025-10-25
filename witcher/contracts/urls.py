from django.urls import path, include 
from . import views
from .views import ContractCreateForm, ContractDetailView



urlpatterns = [
    path("",views.home,name="home"),
    path("login/",views.login_view,name="login"),
    path("logout/",views.logout_view,name="logout"),
    path("signup/",views.SignUp.as_view(),name="signup"),
    path("profile/",views.ProfileView.as_view(),name="profile"),
    path("contracts/<int:pk>/edit/",views.ContractUpdate.as_view(),name="contractupdate"),
    path("contracts/<int:pk>/delete/",views.ContractDelete.as_view(),name="contractdelete"),
    path('contracts/create/',views.ContractCreate.as_view(),name="contractcreate"),
    path('contract/list/', views.ContractList.as_view(),name="contractlist"),
    path('contracts/<slug:slug>/',ContractDetailView.as_view(),name='contractdetail'),
]