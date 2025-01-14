from typing import Any
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models.query import QuerySet
from django.http import HttpRequest

from .models import User, Province, UserProfile

@admin.register(User)
class MyUserAdmin(UserAdmin):
    # edit/view
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone_number', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates',{'fields': ('last_login', 'date_joined')}),
    )
    
    # Add User
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'phone_number', 'password1', 'password2',),
        }),
    )
    
    list_display = ('username', 'phone_number', 'email', 'is_staff')
    search_fields = ('username_exact', )
    ordering = ('id',)
    
    
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('nick_name' ,'gender', 'province')

admin.site.register(Province)

    
    # def get_search_results(self, request: HttpRequest, queryset: QuerySet[Any], search_term):
    #     queryset, may_have_duplicates = super().get_search_results(
    #         request, queryset, search_term,
    #     )
        
        

# Register your models here.
