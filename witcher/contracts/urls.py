from django.urls import path, include 
from . import views
from .views import ContractCreateForm, ContractDetailView
from . import api_views
from rest_framework.authtoken.views import obtain_auth_token


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




    #API
    path("api/token-auth/",obtain_auth_token,name="api_token_auth"),

    path("api/realms/",api_views.realm_list,name="api_realms"),
    path("api/realms/<int:pk>/",api_views.realm_detail,name="api_realm_detail"),

    path("api/towns/",api_views.town_list,name="api_towns"),
    path("api/towns/<int:pk>/",api_views.town_detail,name="api_town_detail"),

    path("api/monsters/",api_views.monster_list,name="api_monsters"),
    path("api/monsters/<int:pk>/",api_views.monster_detail,name="api_monster_detail"),

    path("api/contracts/",api_views.contract_list,name="api_contracts"),
    path("api/contracts/search/",api_views.contract_search,name="api_contracts_search"),
    path("api/contracts/<int:pk>/",api_views.contract_detail,name="api_contract_detail"),
    path("api/contracts/<int:pk>/update/",api_views.contract_update,name="api_contract_update"),
    path("api/contracts/<int:pk>/delete/",api_views.contract_delete,name="api_contract_delete"),
    path("api/contracts/user/me/",api_views.user_contracts,name="api_user_contracts"),

    #required
    path("api/contracts/stats/monthly/",api_views.contracts_stats_monthly,name='api_contracts_stats_monthly'),
    path("api/contracts/user/me/summary/",api_views.user_contracts_summary,name="api_user_contracts_summary"),
]