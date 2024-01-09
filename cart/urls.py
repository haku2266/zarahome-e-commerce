from django.urls import path
from .views import *

app_name = 'cart'

urlpatterns = [

]

htmx_urlpatterns = [
    path('update_cart/<int:product_id>/<str:color>/', cart_update, name='cart_update'),
    path('add/<int:product_id>/', cart_add, name='cart_add'),
    path('plus-quantity/<int:product_id>/<str:color>/', plus_quantity, name='plus_quantity'),
    path('minus-quantity/<int:product_id>/<str:color>/', minus_quantity, name='minus_quantity'),
    path('delete/<int:product_id>/<str:color>/', product_remove, name='product_remove'),
    path('delete_from_nav/<int:product_id>/<str:color>/', product_remove_navbar, name='product_remove_navbar'),

]

urlpatterns += htmx_urlpatterns
