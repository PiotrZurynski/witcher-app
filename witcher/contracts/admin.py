from django.contrib import admin

# Register your models here.
from . models import Realm, Town, Monster, Contract

admin.site.register(Realm)
admin.site.register(Town)
admin.site.register(Monster)
admin.site.register(Contract)


class RealmAdmin(admin.ModelAdmin):
    list_display=("name")

class TownAdmin(admin.ModelAdmin):
    list_display=["name","realm"]

class MonsterAdmin(admin.ModelAdmin):
    list_display=["name","category"]

class ContractAdmin(admin.ModelAdmin):
    list_display=["title","realm","town","monster","reward","currency","state","time_created"]