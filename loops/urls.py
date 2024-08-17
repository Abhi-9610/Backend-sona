from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    # path('',home),
    path('loops/',loopsfun),
    path('events/<str:roboid>/', get_events_by_roboid, name='get_events_by_roboid'),
    path('get_loop/<str:roboid>/', manage_loop, name='manage_loop'),
    path('loopevents/<str:unique_id>/', manage_loopevent, name='manage_loopevent'),
    path('gloop/<str:roboid>/', getloop, name='manage_loop'),
    path('task/',task),
    path('get_task/<str:roboid>/',get_tasks),
    path('manage_task/<str:unique_id>/',manage_task)
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 