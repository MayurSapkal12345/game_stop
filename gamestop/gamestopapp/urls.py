
from django.urls import path
from gamestopapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index),
    path('home', views.home),
    
    path('createproduct', views.create_product),
    path('readproduct', views.read_product),
    path('updateproduct/<rid>', views.update_product),
    path('deleteproduct/<rid>', views.delete_product),
    path('Register', views.user_register),
    path('login', views.user_login),
    path('logout', views.user_logout),
    
    path('create_cart/<rid>', views.create_cart),
    path('readcart', views.read_cart),
    path('delete_cart/<rid>', views.delete_cart),
    path('update_cart/<rid>/<q>', views.update_cart),
    path('create_orders/<rid>', views.create_orders),
    path('readorder', views.read_orders),
    path('create_review/<rid>', views.create_review),
    path('read_product_detail/<rid>', views.read_product_detail),
    path('forgot_password', views.foregot_password),
    path('otp_verification', views.otp_verification),
    
    path('new_password', views.new_password)
    
    
    
    
    
    
  
  
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)