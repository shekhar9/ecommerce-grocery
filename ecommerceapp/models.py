from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from rest_framework import serializers, viewsets, routers
from django.urls import path, include

# Models
class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from rest_framework import serializers, viewsets, routers
from django.urls import path, include

# Models
class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Product(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    sku = models.CharField(max_length=100, unique=True, default='DEFAULT_SKU')
    ean_number = models.CharField(max_length=100, unique=True, blank=True, null=True)
    main_image = models.ImageField(upload_to='products/main/', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    mrp = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    charge_tax = models.BooleanField(default=False)
    stock = models.PositiveIntegerField(default=0)
    weight = models.FloatField(default=0.0)
    weight_unit = models.CharField(max_length=10, default='kg')
    size_in = models.CharField(max_length=10, default='Feet')
    length = models.FloatField(default=0.0)
    width = models.FloatField(default=0.0)
    height = models.FloatField(default=0.0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products", default=1)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True)
    tags = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.TextField(blank=True)
    url_handle = models.CharField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/additional/')

    def __str__(self):
        return f"Image for {self.product.name}"
    

