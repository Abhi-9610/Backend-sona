from django.contrib import admin
from .models import *
# Register your models here.


class Robots(admin.ModelAdmin):
    model=robotModel
    fields=['name','ip','image','owner_id','online','port']
    list_display=['name','ip','image','owner_id','online','port']


admin.site.register(robotModel,Robots)


class Goal(admin.ModelAdmin):
    model=goalsModel
    fields=['name','message','audio','random','owner_id']
    list_display=['name','message','audio','random','owner_id','is_active']

admin.site.register(goalsModel,Goal)