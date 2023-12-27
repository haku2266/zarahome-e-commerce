from django.urls import path, include
from .views import main_view
urlpatterns = [
    path('', main_view, name='main')
]