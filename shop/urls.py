from django.urls import path, include
from .views import (home_view, all_products_view,
                    catalogue_detail_view, product_detail_view,
                    cart_detail_view, search_product, nav_search,
                    item_color_update, item_color_update_2, item_color_update_catalogue)

app_name = 'shop'

urlpatterns = [
    path('', home_view, name='home'),
    path('all-products/<str:filter_by>/', all_products_view, name='all-products'),
    path('catalogue-detail/<str:slug>/', catalogue_detail_view, name='catalogue-detail'),
    path('product-detail/<str:slug>/<str:product_slug>', product_detail_view, name='product-detail'),
    path('cart-detail/', cart_detail_view, name='cart-detail'),
    path('search-product-nav/', nav_search, name='nav-search'),
]

htmx_urlpatterns = [
    path('search-product', search_product, name='search-product'),
    path('item-color-update/<str:slug>/<str:color_code>/', item_color_update, name='item-color-update'),
    path('item-color-update_two/<str:slug>/<str:color_code>/', item_color_update_2, name='item-color-update-two'),
    path('item-color-update_catalogue/<str:slug>/<str:color_code>/', item_color_update_catalogue, name='item-color-update-catalogue')
]

urlpatterns += htmx_urlpatterns
