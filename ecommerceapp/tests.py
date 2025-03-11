from django.test import TestCase
from .models import Order, Product, ReturnedItems
from .serializers import OrderSerializer
from django.contrib.auth.models import User

class OrderSerializerTest(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        # Create a product
        self.product = Product.objects.create(name='Test Product', price=10.00, stock=100)
        
        # Create an order
        self.order = Order.objects.create(user=self.user, product=self.product, quantity=1)
        
        # Create returned items
        self.returned_item = ReturnedItems.objects.create(user=self.user, order=self.order, product=self.product, quantity=1, price=10.00)

    def test_order_serializer(self):
        serializer = OrderSerializer(self.order)
        data = serializer.data
        
        # Check if returned_items field is included and populated
        self.assertIn('returned_items', data)
        self.assertEqual(len(data['returned_items']), 1)  # Expecting one returned item
        self.assertEqual(data['returned_items'][0]['quantity'], 1)  # Check quantity of returned item
        self.assertEqual(data['returned_items'][0]['price'], 10.00)  # Check price of returned item
