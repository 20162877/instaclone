from django.contrib import admin
from .models import User, UserProfile, NetworkEdge


# Register your models here.
class UserPostAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number',)
    list_filter = ('created_on', 'last_update',)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'is_verified',)
    list_filter = ('created_on', 'last_update',)


# admin.site.register(User, UserPostAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(NetworkEdge)
