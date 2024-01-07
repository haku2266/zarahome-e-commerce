from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import ProductModel
from .cart import Cart
from .forms import CartAddProductForm
from render_block import render_block_to_string
from django.http import HttpResponse


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)

    color = request.POST.get('color')
    product = get_object_or_404(ProductModel, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 override_quantity=cd['override'],
                 color=color)
        cart.save()
        html = render_block_to_string('layouts/navbar.html', 'cart-update', context={'cart': cart})
        return HttpResponse(html)
    return render(request, 'home.html')


# @require_POST
# def cart_add_product_detail(request, product_id):
#     cart = Cart(request)
#     form = CartAddProductForm(request.POST)
#     product = get_object_or_404(ProductModel, id=product_id)
#     if form.is_valid():
#         cd = form.cleaned_data
#         cart.add(product=product,
#                  quantity=cd['quantity'],
#                  override_quantity=cd['override'])
#         cart.save()
#         html = render_block_to_string('product-detail.html','', context={'product': product})


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(ProductModel, id=product_id)
    cart.remove(product)
    cart.save()
    return redirect('cart:cart_detail')


@require_POST
def cart_update(request, product_id):
    cart = Cart(request)

    qty = request.POST.get('quantity')
    product = get_object_or_404(ProductModel, id=product_id)

    if not (int(qty) <= 0):
        cart.cart[str(product_id)]['quantity'] = int(qty)
    else:
        cart.remove(product)

    cart.save()
    html = render_block_to_string('cart-detail.html',
                                  'cart-update',
                                  context={'my_cart': cart})
    return HttpResponse(html)


@require_POST
def plus_quantity(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(ProductModel, id=product_id)
    cart.cart[str(product_id)]['quantity'] += 1

    cart.save()

    html = render_block_to_string('cart-detail.html',
                                  'cart-update',
                                  context={'my_cart': cart})
    return HttpResponse(html)


@require_POST
def minus_quantity(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(ProductModel, id=product_id)
    cart.cart[str(product_id)]['quantity'] -= 1
    if cart.cart[str(product_id)]['quantity'] <= 0:
        cart.remove(product)
    cart.save()

    html = render_block_to_string('cart-detail.html',
                                  'cart-update',
                                  context={'my_cart': cart})
    return HttpResponse(html)


@require_POST
def product_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(ProductModel, id=product_id)
    cart.remove(product)
    cart.save()

    html = render_block_to_string('cart-detail.html',
                                  'cart-update',
                                  context={'my_cart': cart})
    return HttpResponse(html)
