from django.contrib.auth.models import Permission
from django.contrib import admin
from dadmin.admin import admin_site

admin_site.register(Permission)