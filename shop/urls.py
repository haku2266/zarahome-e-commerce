from django.urls import path, include
from .views import home_view, all_products_view

app_name = 'shop'

urlpatterns = [
    path('', home_view, name='home'),
    path('all-products/', all_products_view, name='all-products')
]