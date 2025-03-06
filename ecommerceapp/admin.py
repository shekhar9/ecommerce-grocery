from django.contrib import admin
from .models import Product, ProductImage, Order,Category

admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Order)
admin.site.register(Category)  # ✅ Registering the Category model
  # Registering the Order model
