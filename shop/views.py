from django.shortcuts import render
from .models import ProductModel, CategoryModel


def home_view(request):
    new_products = ProductModel.objects.all().order_by('-created_at')[:4]\
        .select_related('class_of_product__type__category').prefetch_related('colors')
    on_sale = ProductModel.objects.filter(sale=True).order_by('-created_at')\
        .select_related('class_of_product__type__category').prefetch_related('colors')

    catalogues = CategoryModel.objects.all().order_by('-created_at')

    return render(request, 'home.html', {'new_products': new_products,
                                         'on_sale_products': on_sale,
                                         'catalogues': catalogues})


def all_products_view(request):
    return render(request, 'all_products.html')


def catalogue_detail_view(request):
    return render(request, 'catalogue-detail.html')


def product_detail_view(request):
    return render(request, 'product-detail.html')


def cart_detail_view(request):
    return render(request, 'cart-detail.html')
