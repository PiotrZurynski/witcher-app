from django.contrib import admin

# Register your models here.
from . models import Realm, Town

admin.site.register(Realm)
admin.site.register(Town)
