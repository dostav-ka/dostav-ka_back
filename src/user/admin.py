from django.contrib import admin

from .models import User, Courier, Manager

admin.site.register(User)
admin.site.register(Courier)
admin.site.register(Manager)
