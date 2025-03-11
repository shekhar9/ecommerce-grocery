from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now  # ✅ Import timezone

from django.utils import timezone

class Category(models.Model):
    title = models.CharField(max_length=255)  # Category Name
    category_head = models.CharField(max_length=255, default='Health & Wellness')  # Category Head
    seller_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Seller Percentage
    media = models.ImageField(upload_to="Categories/", default='Categories/default.jpg')  # Category Image

    def __str__(self):
        return self.title


class Brand(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='brands/', null=True, blank=True)

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
    size_in = models.CharField(max_length=10, default='M')
    length = models.FloatField(default=0.0)
    width = models.FloatField(default=0.0)
    height = models.FloatField(default=0.0)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="products")
    tags = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    rating= models.FloatField(default=0.0)

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




class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shipping_address = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    email = models.EmailField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username


class Banners(models.Model):
    CATEGORY_HEAD_CHOICES = [
        ('Health & Wellness', 'Health & Wellness'),
        ('Electronics', 'Electronics'),
        ('Clothing', 'Clothing'),
        ('Home', 'Home'),
        ('Books', 'Books'),
        ('Toys', 'Toys'),
    ]

    title = models.CharField(max_length=255)
    banner_type = models.CharField(choices=CATEGORY_HEAD_CHOICES, max_length=255)
    image = models.ImageField(upload_to='banners/', null=True, blank=True)





# ✅ Fixed Typo
    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  # ✅ Default value fixed
    fulfilled_orders = models.BooleanField(default=False)  # ✅ Boolean field fixed
    created_at = models.DateTimeField(default=now)
    def returned_items(self):
        return self.returneditems_set.all() 
    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2,)  # ✅ Fix Default Value
    created_at = models.DateTimeField(auto_now_add=True)
    time_to_fulfill = models.DateTimeField(default=timezone.now, null=True, blank=True)



    def __str__(self):
        return f"{self.quantity} of {self.product.name}"



class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    phone_number = models.CharField(max_length=15, blank=True)
    email=models.EmailField(max_length=255, blank=True)
    shipping_address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username


class Sellers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    company_name=models.CharField(max_length=255)
    sellers_business_name=models.CharField(max_length=255)
    image=models.ImageField(upload_to='sellers/', null=True, blank=True)
    company_vatnumber=models.CharField(max_length=255)
    company_number=models.CharField(max_length=255)
    company_address=models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, blank=True)
    email=models.EmailField(max_length=255, blank=True)
    shipping_address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username


class Discount(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateTimeField(default=now)
    combined = models.BooleanField(default=False)
    end_date = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.discount}% off on {self.product.name}"
    


    


class ReturnedItems(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='returned_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # ✅ Fix Default Value
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"