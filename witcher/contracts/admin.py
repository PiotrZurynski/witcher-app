from django.contrib import admin

# Register your models here.
from . models import Realm, Town, Monster, Contract







class RealmAdmin(admin.ModelAdmin):
    list_display=['name']
    search_fields=['name']

admin.site.register(Realm,RealmAdmin)

class TownAdmin(admin.ModelAdmin):
    list_display=['name','realm']
    list_filter=['realm']
    search_fields=['name']

admin.site.register(Town,TownAdmin)

class MonsterAdmin(admin.ModelAdmin):
    list_display=['name','category']
    list_filter=['category']
    search_fields=['name']
    
admin.site.register(Monster,MonsterAdmin)

class ContractAdmin(admin.ModelAdmin):
    list_display=['title','realm','town','monster','reward','currency','state','time_created']
    list_filter=['state','currency','realm','town','monster__category','time_created']
    search_fields=['title','monster__name','town__name']
admin.site.register(Contract,ContractAdmin)