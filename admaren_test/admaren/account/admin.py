from django.contrib import admin
from account.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'name')


admin.site.register(User, UserAdmin)