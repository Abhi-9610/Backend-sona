# urls.py

from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('create-user/', create_subuser, name='create_subuser'),
    path('user-login/', subuser_login, name='subuser_login'),
    path("create-staff/",register_staff),
    path('add-products/',create_products),
    path('admin-profile/',subuser_detail),
    path('getstaff/',staff_detail),
    path('getproducts/',product_detail),
    path('signout/',signout),
    path('updateuser/',updateuser),
    path('updatestaff/<str:unique_id>/',updatestaff),
    path('updateproducts/<str:Products_id>/',update_product),
    path('location/save/',addlocation),
    path('location/get/',getlocation),
    path('location/update/<str:unique_id>/',locationdetails),
    path('location/delete/<str:unique_id>/',locationdetails),
    path('review/',addReview),
    path('get-reviews/',getallReview)
    
  
   
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


