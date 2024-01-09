from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import ProductModel, CategoryModel, ProductClassModel, ProductSizeModel
from cart.forms import CartAddProductForm
from cart.cart import Cart
from django.views.decorators.http import require_POST
from render_block import render_block_to_string
from django.contrib.postgres.search import SearchVector, TrigramSimilarity, SearchQuery, TrigramWordSimilarity
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home_view(request):
    new_products = ProductModel.objects.all().order_by('-created_at')[:4] \
        .select_related('class_of_product__type__category').prefetch_related('variations')
    on_sale = ProductModel.objects.filter(sale=True).order_by('-created_at') \
        .select_related('class_of_product__type__category').prefetch_related('variations')

    form = CartAddProductForm()
    return render(request, 'home.html', {'new_products': new_products,
                                         'on_sale_products': on_sale,
                                         'form': form,
                                         'var': None,
                                         'check': False})


def all_products_view(request, filter_by=None):
    products = ProductModel.objects.all().order_by('-created_at').select_related('class_of_product')
    categories = CategoryModel.objects.all().order_by('-created_at').prefetch_related('types')
    if filter_by == 'sale':
        products = products.filter(sale=True)

    return render(request, 'all_products.html',
                  context={'products': products,
                           'search': None,
                           'categories': categories})


def catalogue_detail_view(request, slug):
    form = CartAddProductForm()
    category = CategoryModel.objects.get(slug=slug)
    products = ProductModel.objects.filter(class_of_product__type__category=category).order_by(
        '-created_at').prefetch_related('class_of_product').prefetch_related('variations__sizes')
    return render(request, 'catalogue-detail.html',
                  context={'category': category,
                           'products': products,
                           'form': form,
                           'var': None,
                           'check': False
                           })


def product_detail_view(request, slug, product_slug=None):
    class_of_product = ProductClassModel.objects.get(slug=slug)
    form = CartAddProductForm()
    products = ProductModel.objects.filter(class_of_product=class_of_product).order_by('-created_at')\
        .prefetch_related('variations').select_related('class_of_product')

    paginator = Paginator(products, 1)

    page_number = request.GET.get('page', 1)

    try:
        products = paginator.page(page_number)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    if product_slug != 'all':
        focus_product = ProductModel.objects.get(slug=product_slug)
        for i in paginator:
            if i.object_list[0] == focus_product:
                products = paginator.page(i.number)

    if request.htmx:
        html = render_block_to_string('product-detail.html', 'product-update',
                                      context={'products': products,
                                               'class_of_product': class_of_product,
                                               'form': form,
                                               'var': None,
                                               'check': False,
                                               'focus_size': None})
        return HttpResponse(html)

    return render(request, 'product-detail.html',
                  context={'products': products,
                           'class_of_product': class_of_product,
                           'form': form})


def cart_detail_view(request):
    my_cart = Cart(request)
    return render(request, 'cart-detail.html', context={'my_cart': my_cart})


def search_product(request):
    search = request.GET.get('search', '')

    if search:
        products = (ProductModel.objects.annotate(search_fields=SearchVector('name', 'class_of_product__name'),
                                                  similarity_name=TrigramSimilarity('name', search),
                                                  similarity_class=TrigramSimilarity('class_of_product__name',
                                                                                     search)).filter(
            Q(search_fields__icontains=search) | Q(similarity_name__gt=0.08) | Q(similarity_class__gt=0.08))).order_by(
            '-similarity_name', '-similarity_class').select_related('class_of_product')

        html = render_block_to_string('all_products.html',
                                      'search-results',
                                      context={'products': products,
                                               'search': search})
        return HttpResponse(html)

    else:

        products = ProductModel.objects.all().order_by('-created_at').select_related('class_of_product')

        html = render_block_to_string('all_products.html',
                                      'search-results',
                                      context={'products': products})
        return HttpResponse(html)


def nav_search(request):
    search = request.GET.get('search', '')
    if search:
        products = (ProductModel.objects.annotate(search_fields=SearchVector('name', 'class_of_product__name'),
                                                  similarity_name=TrigramSimilarity('name', search),
                                                  similarity_class=TrigramSimilarity('class_of_product__name',
                                                                                     search)).filter(
            Q(search_fields__icontains=search) | Q(similarity_name__gt=0.08) | Q(similarity_class__gt=0.08))).order_by(
            '-similarity_name', '-similarity_class').select_related('class_of_product')
        return render(request, 'all_products.html', {'products': products,
                                                     'search': search})


def sidebar_links(request):
    categories = CategoryModel.objects.all()
    return render(request, 'layouts/base.html', {'categories': categories})


def item_color_update(request, slug, color_code=None):
    product = ProductModel.objects.prefetch_related('variations').get(slug=slug)
    form = CartAddProductForm()
    if color_code:
        var = product.variations.get(code=color_code)
        html = render_block_to_string('home.html', 'item-update', context={'var': var,
                                                                           'product': product,
                                                                           'check': True,
                                                                           'form': form})
        return HttpResponse(html)


def item_color_update_2(request, slug, color_code=None):
    product = ProductModel.objects.prefetch_related('variations').get(slug=slug)
    form = CartAddProductForm()

    if color_code:
        var = product.variations.get(code=color_code)
        html = render_block_to_string('home.html', 'item-update-two',
                                      context={
                                          'var': var,
                                          'product': product,
                                          'check': True,
                                          'form': form})
        return HttpResponse(html)


def item_color_update_catalogue(request, slug, color_code=None):
    product = ProductModel.objects.prefetch_related('variations').get(slug=slug)
    form = CartAddProductForm()

    if color_code:
        var = product.variations.get(code=color_code)
        html = render_block_to_string('catalogue-detail.html', 'item-update-catalogue',
                                      context={
                                          'var': var,
                                          'product': product,
                                          'check': True,
                                          'form': form})
        return HttpResponse(html)


def item_color_update_product_detail(request, slug, color_code=None):
    product = ProductModel.objects.prefetch_related('variations').get(slug=slug)
    form = CartAddProductForm()
    if color_code:
        var = product.variations.select_related('product').get(code=color_code)
        html = render_block_to_string('product-detail.html', 'item-update-product',
                                      context={
                                          'var': var,
                                          'product': product,
                                          'check': True,
                                          'form': form})
        return HttpResponse(html)


def size_select(request, size_id, focus_product_id):
    focus_size = ProductSizeModel.objects.get(id=size_id)
    product = ProductModel.objects.get(id=int(focus_product_id))
    html = render_block_to_string('product-detail.html', 'size-btn-update', context={
        'focus_size': focus_size,
        'product': product
    })
    return HttpResponse(html)
