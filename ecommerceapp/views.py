from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Banners
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .models import Product, Order, UserProfile, Category, Brand,Banners
from rest_framework import status
from rest_framework.response import Response
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from ecommerceapp.Serializers import UserRegisterSerializer,ProductSerializer
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from ecommerceapp.forms import LoginForm, RegisterForm, OrderForm, ProductForm, CategoryForm, BrandForm,BnnersForm
from django.contrib.auth.models import User


@csrf_exempt
def inventory_view(request):
    products = Product.objects.all()  # Fetch all products for inventory
    return render(request, 'inventory.html', {'products': products})

@csrf_exempt
def brand_view(request):
    brands = Brand.objects.all()
    return render(request, 'Brand/brand_list.html', {'brands': brands})

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
            return Response('Invalid data', status=status.HTTP_400_BAD_REQUEST)

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
    category_head = request.GET.get('category_head')  # Get the selected category head from the request
    if category_head:
        categories = Category.objects.filter(category_head=category_head)  # Filter categories by selected category head
    else:
        categories = Category.objects.all()  # Fetch all categories if no filter is applied

    return render(request, 'categories.html', {'categories': categories, 'category_heads': Category.CATEGORY_HEAD_CHOICES})  # Pass the categories and category heads to the template

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
            return Response('Invalid data', status=status.HTTP_400_BAD_REQUEST)
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
def order_view(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user  # Set the user to the currently logged-in user
            order.save()
            messages.success(request, 'Order created successfully!')
            return redirect('order_view')  # Redirect to the same page after creating the order
    else:
        form = OrderForm()

    orders = Order.objects.filter(user=request.user)  # Fetch orders for the logged-in user
    return render(request, 'order.html', {'form': form, 'orders': orders})

# Add the new URL for token login


@csrf_exempt

def user_dashboard_api(request):
    products = Product.objects.all()  
    products_data = [{"id": product.id, "name": product.name, "price": product.price, "description": product.description, "stock": product.stock} for product in products]

    return JsonResponse(products_data, safe=False)

def add_product(request, product_id=None):
    is_edit = product_id is not None  # Determine if we are editing an existing product

    if is_edit:
        product = Product.objects.get(id=product_id)  # Retrieve the product to edit
        form = ProductForm(request.POST or None, request.FILES or None, instance=product)  # Populate the form with existing product data
    else:
        form = ProductForm(request.POST, request.FILES or None)  # Instantiate the form for a new product

    if request.method == 'POST' and form.is_valid():
        form.save()  # Save the product
        messages.success(request, 'Product updated successfully!')
        return redirect('admin_dashboard')  # Redirect to admin dashboard after updating

    return render(request, 'add_product.html', {'form': form, 'is_edit': is_edit, 'product': product if is_edit else None})  # Pass the form and is_edit context to the template

@csrf_exempt
def banners_list(request):
    banners1=Banners.objects.all()
    return render(request,'banner/banner.html',{'banners1':banners1})

@csrf_exempt
def add_banner(request, banner_id=None):

    if request.method == 'POST':
        form = BnnersForm(request.POST, request.FILES, instance=banner)  # Populate the form with existing data

        if form.is_valid():
            form.save()
            messages.success(request, 'Bnner is  add successfully!')
            return redirect(banners_list)  # Redirect to the banner list
    else:
        banner = get_object_or_404(Banners, id=banner_id)  # Retrieve the existing banner
        form = BnnersForm(instance=banner)  # Populate the form with existing data for GET request

    
    








class AdminDashboardViewSet(TemplateView):
    template_name = 'admin_dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get('search', '')
        
        context['search_query'] = search_query
        context['products'] = Product.objects.filter(name__icontains=search_query)  # Fetch products matching
        # the search query
        context['is_admin'] = self.request.user.is_staff  # Check if the user is an admin
        
        # Fetch banners to display in the admin dashboard
        context['banners1'] = Banners.objects.all()  # Add this line to include banners
        return context


    def list(self, request):
        products = Product.objects.all()  # Fetch all products
        return Response({"products": products})  # Pass products to the response


class UserRegisterApi(APIView):
    permission_classes=[AllowAny]
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():

            serializer.save()
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
        serializers = ProductSerializer(products, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)
