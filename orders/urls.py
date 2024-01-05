from django.urls import path
from .views import get_orders, create_order
app_name = 'orders'

urlpatterns = [
    path('', get_orders, name='orders'),
    path('create/', create_order, name='create_order')
]