from django.contrib import admin

# Register your models here.
from . models import Realm, Town, Monster, Contract

admin.site.register(Realm)
admin.site.register(Town)
admin.site.register(Monster)
admin.site.register(Contract)
