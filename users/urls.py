from django.urls import path
from .views import register_view, email_validate, password_validate, phone_validate\
    # flag_control

app_name = 'users'

urlpatterns = [
    path('register/', register_view, name='register')
]

htmx_urlpatterns = [
    # path('flag-control/', flag_control, name='flag-control'),
    path('email-validate/', email_validate, name='email-validate'),
    path('password-validate/', password_validate, name='password-validate'),
    path('phone-validate/', phone_validate, name='phone-validate'),
]
urlpatterns += htmx_urlpatterns
