from django.shortcuts import render, redirect
from ecommerceapp.forms import RegisterForm, LoginForm,ProductForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from.models import Product
# Create your views here.
@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login_view')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid username/password')
            return render(request, 'login.html', {'form': LoginForm()})
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

@csrf_exempt
def add_product(request):
    form = ProductForm(request.POST or None)  # Instantiate the form
    if request.method == 'POST' and form.is_valid():
        # Logic to add a product goes here
        form.save()  # Save the product
        messages.success(request, 'Product added successfully!')
        return redirect('admin_dashboard')  # Redirect to admin dashboard after adding
    return render(request, 'add_product.html', {'form': form})  # Pass the form to the template


class AdminDashboardViewSet(TemplateView):
    template_name = 'admin_dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()  # Fetch all products
        return context

    def list(self, request):
        products = Product.objects.all()  # Fetch all products
        return Response({"products": products})  # Pass products to the response
