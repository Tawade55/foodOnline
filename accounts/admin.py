from django.contrib import admin
from .models import User,userprofile
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class CustomUserAdmin(UserAdmin):
    list_display=('email','first_name','last_name','username','role','is_active')
    ordering=('-date_joined',)
    filter_horizontal=() #heh 3 line aahet na 9,10,11    
    list_filter=()      #heh password la non editable karta hashed karun takta ani fielter pan karta name wise,email wise horizontally
    fieldsets=()     


admin.site.register(User,CustomUserAdmin)
admin.site.register(userprofile)
