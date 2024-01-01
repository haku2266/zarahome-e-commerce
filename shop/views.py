from django.shortcuts import render


def home_view(request):
    return render(request, 'home.html')


def all_products_view(request):
    return render(request, 'all_products.html')


def catalogue_detail_view(request):
    return render(request, 'catalogue-detail.html')


def product_detail_view(request):
    return render(request, 'product-detail.html')


def cart_detail_view(request):
    return render(request, 'cart-detail.html')