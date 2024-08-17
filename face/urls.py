# face_recognition_app/urls.py
from django.urls import path
from .views import  get_all_users_info
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('check-face/',get_all_users_info , name='check_or_register_face'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)