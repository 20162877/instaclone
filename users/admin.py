from django.contrib import admin
from .models import Users, UserProfile


# Register your models here.
class UserPostAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', )
    list_filter = ('created_on', 'last_update', )


admin.site.register(Users, UserPostAdmin)
admin.site.register(UserProfile)
