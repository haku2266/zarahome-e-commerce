from django.urls import path, include
from .views import (home_view, all_products_view,
                    catalogue_detail_view, product_detail_view,
                    cart_detail_view)

app_name = 'shop'

urlpatterns = [
    path('', home_view, name='home'),
    path('all-products/', all_products_view, name='all-products'),
    path('catalogue-detail/', catalogue_detail_view, name='catalogue-detail'),
    path('product-detail/', product_detail_view, name='product-detail'),
    path('cart-detail/', cart_detail_view, name='cart-detail'),
]