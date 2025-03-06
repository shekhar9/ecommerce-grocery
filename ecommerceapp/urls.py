from django.urls import path
from . import views
from .views import UserRegisterApi, TokenLoginView, UserLogoutView,UserDashboardApi,banners_list

urlpatterns = [  
    path('banners/', banners_list, name='banners_list'),  # Add this line for the banners list

    path('categories/', views.categories_view, name='categories'),
    path('add_category/', views.add_category, name='add_category'),
    path('edit_category/<int:category_id>/', views.add_category, name='edit_category'),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),  # New delete category path
    path('brands/', views.brand_view, name='brands'),
    path('add_brand/', views.add_brand, name='add_brand'),
    path('edit_brand/<int:brand_id>/', views.add_brand, name='edit_brand'),
    path('delete_brand/<int:brand_id>/', views.delete_brand, name='delete_brand'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('order/', views.order_view, name='order_view'),
    path('inventory/', views.inventory_view, name='inventory_view'),
    path('brand/', views.brand_view, name='brand_view'),
    path('admin_dashboard/', views.AdminDashboardViewSet.as_view(), name='admin_dashboard'),

    path('add_product/<int:product_id>/', views.add_product, name='edit_product'),
    path('edit_product/', views.add_product, name='add_product'),

    path('user_dashboard_api/', views.user_dashboard_api, name='user_dashboard_api'),
    path('api/register/', UserRegisterApi.as_view(), name='user_register'),
    path('api/login/', TokenLoginView.as_view(), name='user_login'),
    path('api/logout/', UserLogoutView.as_view(), name='user_logout'),
    path('api/user_dashboard/', UserDashboardApi.as_view(), name='user_dashboard'),
    
]
