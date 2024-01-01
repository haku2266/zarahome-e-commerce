from django.urls import path
from .views import get_orders
app_name = 'orders'

urlpatterns = [
    path('', get_orders, name='orders')
]