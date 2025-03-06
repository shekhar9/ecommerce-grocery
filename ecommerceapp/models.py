from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    CATEGORY_HEAD_CHOICES = [
        ('Health & Wellness', 'Health & Wellness'),
        ('Electronics', 'Electronics'),
        ('Clothing', 'Clothing'),
        ('Home', 'Home'),
        ('Books', 'Books'),
        ('Toys', 'Toys'),
    ]

    title = models.CharField(max_length=255)  # Category Name

    category_head = models.CharField(
        max_length=255, 
        choices=CATEGORY_HEAD_CHOICES, 
        default='Health & Wellness'
    )  # Category Head

    seller_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Seller Percentage
    media=models.ImageField(upload_to="Categories/",default='Categories/default.jpg') # Category Image

    def __str__(self):
        return self.title


# Models

class Product(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]
    
    
    BRAND_CHOICES= [
        ('Nike', 'Nike'),
        ('Adidas', 'Adidas'),
        ('Burberry', 'Burberry'),
        ('Puma', 'Puma'),
        ('Gucci', 'Gucci'),
        ('Louis Vuitton', 'Louis Vuitton'),
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
    brand = models.CharField(max_length=50, choices=BRAND_CHOICES, default='Nike')
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

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shipping_address = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    email = models.EmailField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username
    


class  Brand(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='brands/', null=True, blank=True)
    def __str__(self):
        return self.name


class Banners(models.Model):
    CATEGORY_HEAD_CHOICES = [
        ('Health & Wellness', 'Health & Wellness'),
        ('Electronics', 'Electronics'),
        ('Clothing', 'Clothing'),
        ('Home', 'Home'),
        ('Books', 'Books'),
        ('Toys', 'Toys'),
    ]

    title=models.CharField(max_length=255)
    banner_type=models.CharField(max_length=255,choices=CATEGORY_HEAD_CHOICES)
    image=models.ImageField(upload_to='banners/',null=True,blank=True)
