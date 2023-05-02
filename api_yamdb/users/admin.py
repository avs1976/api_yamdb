from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'email', 'role',
                    'bio', 'first_name', 'last_name')
    search_fields = ('username', 'email', 'role')
    list_filter = ('role',)


admin.site.register(User, UserAdmin)
