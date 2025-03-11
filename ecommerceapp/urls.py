from django.urls import path
from . import views
from .views import UserRegisterApi, TokenLoginView, UserLogoutView,UserDashboardApi,banners_list,OrderViewSet,admin_order_list,ReturnedItemsView,admin_logout,add_sellers,sellers_list1,Sellers_listApi
from ecommerceapp.views import *
urlpatterns = [  
    path('banners/', banners_list, name='banners_list'), 
    path('add_banner/',views.add_banner,name='add_banner'), # Add this line for the banners list
    path('edit_banner/<int:banner_id>/', views.add_banner, name='edit_banner'),
    path('delete_banner/<int:banner_id>/',views.delete_banner,name='delete_banner'),
    path('admin_logout/', admin_logout, name='admin_logout'),  # Add this line for the admin logout
    path('categories/', views.categories_view, name='categories'),
    path('add_category/', views.add_category, name='add_category'),
    path('edit_category/<int:category_id>/', views.add_category, name='edit_category'),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('brands/', views.brand_view, name='brands'),
    path('add_brand/', views.add_brand, name='add_brand'),
    path('edit_brand/<int:brand_id>/', views.add_brand, name='edit_brand'),
    path('delete_brand/<int:brand_id>/', views.delete_brand, name='delete_brand'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('inventory/', views.inventory_view, name='inventory_view'),
    path('brand/', views.brand_view, name='brand_view'),
    path('admin_dashboard/', views.AdminDashboardViewSet.as_view(), name='admin_dashboard'),
    path('products/', views.product_list, name='product_list'),
    path('add_product/<int:product_id>/', views.add_product, name='edit_product'),
    path('edit_product/', views.add_product, name='add_product'),

    path('user_dashboard_api/', views.user_dashboard_api, name='user_dashboard_api'),
    path('api/register/', UserRegisterApi.as_view(), name='user_register'),
    path('api/login/', TokenLoginView.as_view(), name='user_login'),
    path('api/logout/', UserLogoutView.as_view(), name='user_logout'),
    path('api/user_dashboard/', UserDashboardApi.as_view(), name='user_dashboard'),
    path('orders/', admin_order_list, name='admin_order_list'),  # ✅ Order list page for users
    path('order/<int:order_id>/', views.admin_order_list, name='order_detail'), 
    path('return_item/', ReturnedItemsView.as_view(), name='return_item'),  # ✅ Return item page]
    path('api/orders/', OrderViewSet.as_view(), name='order_api'),  # ✅ Change API URL name
    path('customers/', views.customer_list, name='customer_list'),
    path('admin_logout/',views.admin_logout,name='admin_logout'),
    path('add_sellers/',views.add_sellers,name='add_sellers'),
    path('sellers_list1/',views.sellers_list1,name='sellers_list1'),
    path('api/sellers_list/',Sellers_listApi.as_view(),name='sellers_list'),
    path('user_dashbord1/',views.user_dashbord1,name='user_dashbord1'),
    path('discount/',views.discount,name='discount'),
    path('dicount_list/',views.discount_list,name='discount_list'),



]

from django.urls import path
order_api_urls = [
    path('api/orders/', OrderViewSet.as_view(), name='order_api'),  # ✅ Change API URL name
]
