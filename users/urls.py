from django.urls import path
from .views import register_view, flag_control

app_name = 'users'

urlpatterns = [
    path('register/', register_view, name='register')
]

htmx_urlpatterns = [
    path('flag-control/', flag_control, name='flag-control')
]
urlpatterns += htmx_urlpatterns
