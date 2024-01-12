from django.urls import path
from .views import get_orders, create_order, check_promo

app_name = 'orders'

urlpatterns = [
    path('', get_orders, name='orders'),
    path('create/', create_order, name='create_order'),
    path('promo_check/', check_promo, name='check_promo')
]
