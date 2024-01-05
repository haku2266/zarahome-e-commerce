from django.http import HttpResponse
from django.shortcuts import render
from .models import ProductModel, CategoryModel
from cart.forms import CartAddProductForm
from cart.cart import Cart
from django.views.decorators.http import require_POST
from render_block import render_block_to_string
from django.contrib.postgres.search import SearchVector, TrigramSimilarity, SearchQuery, TrigramWordSimilarity
from django.db.models import Q


def home_view(request):
    new_products = ProductModel.objects.all().order_by('-created_at')[:4] \
        .select_related('class_of_product__type__category').prefetch_related('colors')
    on_sale = ProductModel.objects.filter(sale=True).order_by('-created_at') \
        .select_related('class_of_product__type__category').prefetch_related('colors')

    catalogues = CategoryModel.objects.all().order_by('-created_at')
    form = CartAddProductForm()
    return render(request, 'home.html', {'new_products': new_products,
                                         'on_sale_products': on_sale,
                                         'catalogues': catalogues,
                                         'form': form})


def all_products_view(request, filter_by=None):
    products = ProductModel.objects.all().order_by('-created_at')
    if filter_by == 'sale':
        products = products.filter(sale=True)

    return render(request, 'all_products.html', context={'products': products,
                                                         'search': None})


def catalogue_detail_view(request):
    return render(request, 'catalogue-detail.html')


def product_detail_view(request):
    return render(request, 'product-detail.html')


def cart_detail_view(request):
    my_cart = Cart(request)
    return render(request, 'cart-detail.html', context={'my_cart': my_cart})


# @require_POST
def search_product(request):
    search = request.GET.get('search', '')

    if search:
        products = (ProductModel.objects.annotate(search_fields=SearchVector('name', 'class_of_product__name'),
                                                  similarity=TrigramSimilarity('name', search)).filter(
            Q(search_fields__icontains=search) | Q(similarity__gt=0.1))).order_by('-similarity')

        html = render_block_to_string('all_products.html',
                                      'search-results',
                                      context={'products': products,
                                               'search': search})
        return HttpResponse(html)

    # elif request.path.split('/')[-1] == 'sale':
    #     products = ProductModel.objects.filter(sale=True)
    #
    #     html = render_block_to_string('all_products.html',
    #                                   'search-results',
    #                                   context={'products': products, 'search': search})
    else:

        products = ProductModel.objects.all().order_by('-created_at')

        html = render_block_to_string('all_products.html',
                                      'search-results',
                                      context={'products': products})
        return HttpResponse(html)
