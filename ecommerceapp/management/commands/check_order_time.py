from django.core.management.base import BaseCommand
from ecommerceapp.models import Order

class Command(BaseCommand):
    help = 'Check the time_to_fulfill values in the Order model'

    def handle(self, *args, **kwargs):
        orders = Order.objects.all()
        for order in orders:
            print(f'Order ID: {order.id}, time_to_fulfill: {order.time_to_fulfill}')
