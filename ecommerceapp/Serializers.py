from rest_framework import serializers
from .models import Product, Order, UserProfile, OrderItem, ReturnedItems,Sellers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from ecommerceapp.models import Customer  # ✅ Import Customer model
import re  # Import regex for password validation

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'main_image']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'
    
class ReturnedItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReturnedItems
        fields = '__all__'


class UserRegisterSerializer(serializers.ModelSerializer):
    mobile_number = serializers.CharField(max_length=10, write_only=True)
    address = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'mobile_number', 'address']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, value):
        # Check password length
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        # Check for complexity
        if not re.search(r"[A-Z]", value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r"[0-9]", value):
            raise serializers.ValidationError("Password must contain at least one digit.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise serializers.ValidationError("Password must contain at least one special character.")
        return value

    def create(self, validated_data):
        mobile_number = validated_data.pop('mobile_number')
        address = validated_data.pop('address')
        email = validated_data.get('email')

        # ✅ Create User
        user = User.objects.create_user(**validated_data)

        # ✅ Check if Customer already exists before creating
        customer, created = Customer.objects.get_or_create(user=user, defaults={
            'phone_number': mobile_number,
            'shipping_address': address,
            'email': email
        })

        if not created:
            # Customer already exists, update fields instead of inserting again
            customer.phone_number = mobile_number
            customer.shipping_address = address
            customer.save()

        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class OrderSerializer(serializers.ModelSerializer):
    returned_items = serializers.SerializerMethodField()  # ✅ Fetch related returned items properly
    user = UserRegisterSerializer(read_only=True)  # Show full user details
    product = ProductSerializer(read_only=True)  # Show full product details
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source="product", write_only=True
    )  # Allow passing only product_id in requests

    class Meta:
        model = Order
        fields = ['id', 'user', 'product', 'product_id', 'quantity', 'fulfilled_orders', 'created_at', 'returned_items']
        read_only_fields = ['user']  # ✅ Keep only one read_only_fields declaration

    def get_returned_items(self, obj):
        """
        Fetch and serialize the related returned items for an order.
        """
        returned_items = obj.returned_items.all()  # ✅ Ensure related_name exists in model
        return ReturnedItemsSerializer(returned_items, many=True).data  # ✅ Serialize related items


class ReturnedItemsSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField(write_only=True)
    product_id = serializers.IntegerField(write_only=True)
    user = serializers.StringRelatedField(read_only=True)  # ✅ Display user as a string

    class Meta:
        model = ReturnedItems
        fields = ['id', 'user', 'order_id', 'product_id', 'quantity', 'price', 'created_at']

    def create(self, validated_data):
        request = self.context.get('request')
        
        # ✅ Ensure request exists and user is authenticated
        if not request or not hasattr(request, "user") or not request.user.is_authenticated:
            raise serializers.ValidationError({'error': 'User is not authenticated'})

        order_id = validated_data.pop('order_id')
        product_id = validated_data.pop('product_id')

        try:
            order = Order.objects.get(id=order_id)
            product = Product.objects.get(id=product_id)
        except Order.DoesNotExist:
            raise serializers.ValidationError({'order_id': 'Invalid order ID'})
        except Product.DoesNotExist:
            raise serializers.ValidationError({'product_id': 'Invalid product ID'})

        # ✅ Ensure the returned item belongs to the same user
        if order.user != request.user:
            raise serializers.ValidationError({'order_id': 'You can only return items from your own orders'})

        # ✅ Save the user who returned the item
        returned_item = ReturnedItems.objects.create(
            user=request.user,
            order=order,
            product=product,
            **validated_data
        )
        return returned_item


class Sellersserializers(serializers.ModelSerializer):
    class Meta:
        model = Sellers
        fields ='__all__'
