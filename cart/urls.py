from django.urls import path
from .views import *

app_name = 'cart'

urlpatterns = [

]

htmx_urlpatterns = [
    path('update_cart/<int:product_id>/', cart_update, name='cart_update'),
    path('add/<int:product_id>/', cart_add, name='cart_add'),
    path('remove/<int:product_id>/', cart_remove, name='cart_remove'),
    path('plus-quantity/<int:product_id>/', plus_quantity, name='plus_quantity'),
    path('minus-quantity/<int:product_id>/', minus_quantity, name='minus_quantity'),
    path('delete/<int:product_id>/', product_remove, name='product_remove')

]

urlpatterns += htmx_urlpatterns
