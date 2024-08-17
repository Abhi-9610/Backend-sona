from django.contrib import admin
from .models import *
# Register your models here.
class Loop(admin.ModelAdmin):
    model=loops
    fields=['timestring','time_delay_seconds','type','name','admin_id','roboid']
    list_display=['name','timestring','time_delay_seconds','type','admin_id','roboid']


admin.site.register(loops,Loop)


class LoopEvent(admin.ModelAdmin):
    model=loopevent
    fields=['goalid','type','owner_id']
    list_display=['goalid','type','owner_id']

admin.site.register(loopevent,LoopEvent)