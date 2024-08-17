from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from .models import CustomUser, ProductsModels
from robot.models import robotModel
from robot.serializers import *

# Inline class for robotModel
class RobotModelInline(admin.TabularInline):  # or use StackedInline for a different display style
    model = robotModel
    extra = 0

    def get_queryset(self, request: HttpRequest):
        new=super().get_queryset(request)
        roboid = request.GET.get('unique_id', None)

        if roboid:
            # Filter the queryset based on the 'unique_id' parameter
            queryset = new.filter(unique_id=roboid)
            print(queryset)
 
    
# class ProductsModelsInline(admin.TabularInline):  # or admin.StackedInline
#     model = ProductsModels
#     extra = 1

class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    fields = ['name', 'mobile', 'email', 'profile', 'is_active', 'role']
    list_display = ['name', 'mobile', 'email', 'profile', 'is_active', 'role', 'created_at']
    inlines = [RobotModelInline]  # Add the RobotModelInline to display associated robotModel objects

    def get_queryset(self, request):
        # Override get_queryset to exclude superusers
        queryset = super().get_queryset(request)
        new=queryset[0].unique_id
     #    print(new)
       
        return queryset.exclude(is_superuser=True)

admin.site.register(CustomUser, CustomUserAdmin)

class ProductAdmin(admin.ModelAdmin):
    model = ProductsModels
    fields = ['name', 'image', 'desc', 'owner_id']
    list_display = ['name', 'image', 'desc', 'created_at']

admin.site.register(ProductsModels, ProductAdmin)
