from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home),
    path('addrobot/', addrobot),
    path('addgoal/', addgoals),
    path('robots/<str:unique_id>/', robot_detail, name='robot_detail'),
    path('goals/<str:unique_id>/', goal_detail, name='goal_detail'),
    path('getgoal/', goaldetail),
    path('getrobo/', robotdetail,name='name'),
    
] +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
