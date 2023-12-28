from django.shortcuts import render


def home_view(request):
    return render(request, 'home.html')


def all_products_view(request):
    return render(request, 'all_products.html')
