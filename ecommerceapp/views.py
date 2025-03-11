from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.decorators import api_view, permission_classes

from django.contrib import messages
from .models import Banners
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import Product, UserProfile, Category, Brand, Banners, Order, Customer, OrderItem, ReturnedItems, Sellers,Discount
from rest_framework import status
from rest_framework.response import Response
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from ecommerceapp.Serializers import UserRegisterSerializer, ProductSerializer, OrderSerializer, OrderItemSerializer, ReturnedItemsSerializer, Sellersserializers
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from ecommerceapp.forms import LoginForm, RegisterForm, ProductForm, CategoryForm, BrandForm, BannersForm, SellersForms,DiscountForm
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import requests
from .pagination import CustomPagination
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory

@csrf_exempt
def banners_list(request):
    search_query = request.GET.get('search', '')  # Get the search query from the request
    banners1 = Banners.objects.all()  # Fetch all banners

    if search_query:
        banners1 = banners1.filter(title__icontains=search_query)  # Filter banners by title

    return render(request, 'banner/banner.html', {'banners1': banners1, 'search_query': search_query})

@csrf_exempt
def inventory_view(request):
    products = Product.objects.all()  # Fetch all products for inventory
    return render(request, 'inventory.html', {'products': products})

@csrf_exempt
def brand_view(request):
    search_query = request.GET.get('search', '')  # Get the search query from the request
    brands = Brand.objects.all()  # Fetch all brands

    if search_query:
        brands = brands.filter(name__icontains=search_query)  # Filter brands by name

    page = request.GET.get('page', 1)
    paginator = Paginator(brands, 10)
    try:
        brands = paginator.page(int(page))  # Convert page number to integer
    except PageNotAnInteger:
        brands = paginator.page(1)
    except EmptyPage:
        brands = paginator.page(paginator.num_pages)
    return render(request, 'Brand/brand_list.html', {'brands': brands, 'search_query': search_query})


@csrf_exempt
def add_brand(request, brand_id=None):
    if brand_id:
        brand = Brand.objects.get(id=brand_id)
        form = BrandForm(request.POST or None, request.FILES or None, instance=brand)  # Populate the form with existing data
        is_edit = True  # Set is_edit to True for editing
    else:
        form = BrandForm(request.POST or None, request.FILES or None)  # Instantiate an empty form
        is_edit = False  # Set is_edit to False for adding

    if request.method == 'POST':
        if form.is_valid():
            brand = form.save()
            return redirect('brand_view')
        else:
            return render(request, 'Brand/brand.html', {'form': form, 'is_edit': is_edit, 'brand': brand if brand_id else None})  # Pass brand to the template

    return render(request, 'Brand/brand.html', {'form': form, 'is_edit': is_edit, 'brand': brand if brand_id else None})  # Pass brand to the template

@csrf_exempt
def delete_brand(request, brand_id):
    try:
        brand = Brand.objects.get(id=brand_id)
        brand.delete()  # Delete the brand
        messages.success(request, 'Brand deleted successfully!')
    except Brand.DoesNotExist:
        messages.error(request, 'Brand not found.')
    return redirect('brands')

@csrf_exempt
def categories_view(request):
    category_head = request.GET.get('category_head', '')  # Get the selected category head from request
    categories = Category.objects.all()  # Fetch all categories from database
    
    if category_head:
        categories = categories.filter(category_head__icontains=category_head)  # Filter categories

    # Pagination
    page = request.GET.get('page', 1)  # Get page number safely
    paginator = Paginator(categories, 10)  # Show 10 categories per page

    try:
        paginated_categories = paginator.page(page)
    except PageNotAnInteger:
        paginated_categories = paginator.page(1)  # If page is not an integer, show first page
    except EmptyPage:
        paginated_categories = paginator.page(paginator.num_pages)  # If out of range, show last page

    category_heads = Category.objects.values_list('category_head', flat=True).distinct()  # Get distinct category heads

    return render(request, 'categories.html', {'categories': paginated_categories, 'category_heads': category_heads})

def add_category(request, category_id=None): 
    form = CategoryForm(request.POST or None, request.FILES or None)  # Instantiate an empty form
    if category_id:
        category = Category.objects.get(id=category_id)  # Retrieve the existing category
        form = CategoryForm(request.POST or None, request.FILES or None, instance=category)  # Populate the form with existing data

    if request.method == 'POST':
        if form.is_valid():
            form.save()  # Update the existing category
            messages.success(request, 'Category updated successfully!')
            return redirect('categories')
        else:
            print("Form Errors:", form.errors) 

    return render(request, 'add_category.html', {'form': form})  # Pass the form

@csrf_exempt
def delete_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
        category.delete()  # Delete the category
        messages.success(request, 'Category deleted successfully!')
    except Category.DoesNotExist:
        messages.error(request, 'Category not found.')
    return redirect('categories')  # Redirect to the categories page

@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_profile = UserProfile.objects.create(user=user)  # Create user profile
            return redirect('login_view') 
        else:
            return render(request, 'register.html', {'form': form})  # Pass the form
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@csrf_exempt
def logout_view(request):
    logout(request)
    return redirect('login_view')

@csrf_exempt
def user_dashboard_api(request):
    products = Product.objects.all()  
    products_data = [{"id": product.id, "name": product.name, "price": product.price, "description": product.description, "stock": product.stock} for product in products]

    return JsonResponse(products_data, safe=False)

from django.shortcuts import get_object_or_404

def add_product(request, product_id=None):
    is_edit = product_id is not None  

    if is_edit:
        product = get_object_or_404(Product, id=product_id)
        form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    else:
        form = ProductForm(request.POST, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        product = form.save(commit=False)  

        category_head = form.cleaned_data['category_head']  # This now gives a Category object
        product.category = category_head  # Directly assign the Category object

        product.save()  
        messages.success(request, 'Product updated successfully!')
        return redirect('admin_dashboard')  

    category_heads = Category.objects.values_list('category_head', flat=True).distinct()

    return render(request, 'add_product.html', {'form': form, 'is_edit': is_edit, 'product': product if is_edit else None, 'category_heads': category_heads})  # Pass the form, is_edit context, and category heads to the template

@csrf_exempt
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

@csrf_exempt
def add_banner(request, banner_id=None):
    if request.method == 'POST':
        if banner_id:
            banner = get_object_or_404(Banners, id=banner_id)  # Retrieve the existing banner
            form = BannersForm(request.POST, request.FILES, instance=banner)  # Populate the form with existing data
        else:
            form = BannersForm(request.POST, request.FILES)  # Instantiate an empty form

        if form.is_valid():
            form.save()
            messages.success(request, 'Banner is added successfully!')
            return redirect(banners_list)  # Redirect to the banner list
        else:
            # Return the form with errors if invalid
            return render(request, 'banner/add_banner.html', {'form': form})  # Render the form with errors
    else:
        if banner_id:
            banner = get_object_or_404(Banners, id=banner_id)  # Retrieve the existing banner
            form = BannersForm(instance=banner)  # Populate the form with existing data for GET request
        else:
            form = BannersForm()  # Instantiate an empty form

    return render(request, 'banner/add_banner.html', {'form': form})  # Render the form

@csrf_exempt
def delete_banner(request, banner_id):

    try:
        banner = Banners.objects.get(id=banner_id)

        banner.delete()  # Delete the category
        messages.success(request, 'Category deleted successfully!')
    except Category.DoesNotExist:
        messages.error(request, 'Category not found.')
    return redirect('banners_list') 

class AdminPagenation(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class AdminDashboardViewSet(TemplateView):
    template_name = 'admin_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get('search', '')

        # 🔹 Convert `page_number` to integer safely
        try:
            product_page_number = int(self.request.GET.get('product_page', 1))
            user_page_number = int(self.request.GET.get('user_page', 1))
        except ValueError:
            product_page_number = user_page_number = 1  # Default to first page if invalid

        # 🔹 Fetch products matching the search query
        product_list = Product.objects.filter(name__icontains=search_query)

        # 🔹 Fetch all normal users (non-admin users)
        user_list = User.objects.filter(is_staff=False)

        # 🔹 Paginate Products (10 per page)
        product_paginator = Paginator(product_list, 10)
        user_paginator = Paginator(user_list, 10)

        try:
            products = product_paginator.page(product_page_number)
        except (PageNotAnInteger, EmptyPage):
            products = product_paginator.page(1)  # Show first page if invalid

        try:
            users = user_paginator.page(user_page_number)
        except (PageNotAnInteger, EmptyPage):
            users = user_paginator.page(1)  # Show first page if invalid

        # Add paginated data to context
        context['search_query'] = search_query
        context['products'] = products  # Paginated products
        context['users'] = users  # Paginated normal users
        context['is_admin'] = self.request.user.is_staff
        context['banners1'] = Banners.objects.all()  # Add banners to the context

        return context

@csrf_exempt
def admin_logout(request):
    logout(request)
    return redirect('login_view')

class UserRegisterApi(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()  # The serializer handles User & Customer creation
            
            return JsonResponse(serializer.data, status=201)

        return JsonResponse(serializer.errors, status=400)

class TokenLoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid username/password'}, status=status.HTTP_400_BAD_REQUEST)

class UserLogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'message': 'User logged out successfully'}, status=status.HTTP_200_OK)

class UserDashboardApi(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = Product.objects.all()

        # Get query parameters
        name=request.query_params.get('name', None)
       
        brand_name = request.query_params.get('brand', None)
        category_head = request.query_params.get('category', None)
        rating=request.query_params.get('rating',None)

        # Apply filters
        if brand_name:
            products = products.filter(brand__name__iexact=brand_name)  # Exact match for brand

        if category_head:
            print(f"Filtering products where category__category_head = {category_head}")  # Debug print
            products = products.filter(category__category_head__iexact=category_head)
          # Exact match for category
        if rating:
            products = products.filter(rating__gte=rating)  # Filter products with rating >=

        if name:
            products = products.filter(name__iexact=name)
        
        # Debugging output
        print(f"Filtered products count: {products.count()}")

        # Serialize and return response
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class OrderPagination(PageNumberPagination):
    page_size = 2  # Default items per page
    page_size_query_param = 'page_size'
    max_page_size = 100

class OrderViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # ✅ Fetch orders based on user type
        if request.user.is_staff:
            orders = Order.objects.all().order_by('-created_at').prefetch_related('returned_items')
            returned_items = ReturnedItems.objects.all()
        else:
            orders = Order.objects.filter(user=request.user).order_by('-created_at').prefetch_related('returned_items')
            returned_items = ReturnedItems.objects.filter(order__in=orders)

        # ✅ Serialize data
        order_serializer = OrderSerializer(orders, many=True)
        returned_serializer = ReturnedItemsSerializer(returned_items, many=True)

        return Response({
            "orders": order_serializer.data,
            "returned_items": returned_serializer.data
        })

from django.contrib.auth.decorators import user_passes_test

import requests
from rest_framework.authtoken.models import Token
from django.contrib.auth.decorators import user_passes_test

def is_admin(user):
    return user.is_staff or user.is_superuser

@user_passes_test(is_admin)
def admin_order_list(request):
    # 🔹 Get admin API token
    try:
        token = Token.objects.get(user=request.user).key
    except Token.DoesNotExist:
        return render(request, "error.html", {"message": "Admin user has no API token."})

    # 🔹 Fetch all orders from API
    api_url = "http://127.0.0.1:8000/api/orders/"
    headers = {"Authorization": f"Token {token}"}
    response = requests.get(api_url, headers=headers)

    # 🔹 Validate API response
    if response.status_code == 200:
        orders_data = response.json()
        orders = orders_data.get("orders", [])  # ✅ Extract results
        returned_items = orders_data.get("returned_items", [])
    else:
        orders = []
        returned_items = []

    # 🔹 Debug: Print response
    print(f"Orders Data: {orders}")  
    print(f"Returned Items Data: {returned_items}")

    # 🔹 Pass data to the template
    return render(request, "order.html", {
        "orders": orders,
        "returned_items": returned_items
    })

class ReturnedItemsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ReturnedItemsSerializer(data=request.data, context={'request': request})  # ✅ Pass request context
        if serializer.is_valid():
            returned_item = serializer.save()
            return Response(ReturnedItemsSerializer(returned_item).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        returned_items = ReturnedItems.objects.all()
        serializer = ReturnedItemsSerializer(returned_items, many=True)
        return Response(serializer.data)

def customer_list(request):
    customers = Customer.objects.all()  # Fetch all customers
    return render(request, 'customer_list.html', {'customers': customers})

@csrf_exempt
def add_sellers(request, sellers_id=None):
    if request.method == 'POST':
        if sellers_id:
            seller = get_object_or_404(Sellers, id=sellers_id)

            form = SellersForms(request.POST, request.FILES, instance=seller)

        else:
            form=SellersForms(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Sellers Add sucesfully')
            return redirect('add_sellers')
        else:
            return render(request,'sellers.html',{'form':form})

        
    else:
        if sellers_id:
            seller=get_object_or_404(Sellers,id=sellers_id)
            form=SellersForms(initial=seller)
        else:
            form=SellersForms()
    return render(request, 'sellers.html', {'form': form})  # Render the form

@csrf_exempt
def sellers_list1(request):
    sellers = Sellers.objects.all()  # Fetch all sellers
    return render(request, 'Sellers/sellers_list.html', {'sellers': sellers})  # Render

class Sellers_listApi(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request):
        sellers = Sellers.objects.all()
        serializer = Sellersserializers(sellers, many=True)
        return Response(serializer.data)

@csrf_exempt
def user_dashbord1(request):
    sellers=Sellers.objects.all()
    return render(request,'userdashbord.html',{'sellers':sellers})


@csrf_exempt
def discount(request,discount_id=None):
    if request.method == 'POST':
        discount = Discount.objects.create()
        form = DiscountForm(request.POST, instance=discount)
        if form.is_valid():
            form.save()
            messages.success(request,'Discount Add sucesfully')
            return redirect('discount')
        else:
            return render(request,'Discount/discount.html',{'form':form})
    else:
        if discount_id:
            discount = get_object_or_404(Discount, id=discount_id)
            form = DiscountForm(initial=discount)
        else:
            form = DiscountForm()
    return render(request,'Discount/discount.html',{'form':form})


@csrf_exempt
def discount_list(request):
    discount=Discount.objects.all()
    return render(request,'Discount/discount_list.html',{'discount':discount})

