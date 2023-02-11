from django.contrib import admin

from server.apps.accounts.models import User

admin.site.register(User)
