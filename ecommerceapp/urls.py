from django.urls import path,include
from ecommerceapp.views import *
from django.urls import path
from ecommerceapp.views import AdminDashboardViewSet


urlpatterns = [

    # Other URL patterns...
    path('add_product/', add_product, name='add_product'),

    path('admin_dashboard/', AdminDashboardViewSet.as_view(), name='admin_dashboard'),

   path('register/',register,name='register'),
   path('login_view/',login_view,name='login_view')
]
