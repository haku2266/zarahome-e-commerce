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
    size = request.POST.get('size')
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 override_quantity=cd['override'],
                 color=color,
                 size=size)
        cart.save()
        html = render_block_to_string('layouts/navbar.html', 'cart-update', context={'cart': cart})
        return HttpResponse(html)
    return render(request, 'home.html')


@require_POST
def cart_update(request, product_id, color=None):
    cart = Cart(request)

    qty = request.POST.get('quantity')
    product = get_object_or_404(ProductModel, id=product_id)

    if not (int(qty) <= 0):
        if color is not None and color != 'None':
            cart.cart[str(product_id)]['colors'][color]['item_quantity'] = int(qty)
            cart.cart[str(product_id)]['quantity'] = sum(
                [q_s['item_quantity'] for color, q_s in cart.cart[str(product_id)]['colors'].items()])
        else:
            cart.cart[str(product_id)]['quantity'] = int(qty)
    else:
        if color is not None and color != 'None':
            del cart.cart[str(product_id)]['colors'][color]
            cart.cart[str(product_id)]['quantity'] = sum(
                [q_s['item_quantity'] for color, q_s in cart.cart[str(product_id)]['colors'].items()])
        else:
            del cart.cart[str(product_id)]
    cart.save()
    html = render_block_to_string('cart-detail.html',
                                  'cart-update',
                                  context={'my_cart': cart})
    return HttpResponse(html)


@require_POST
def plus_quantity(request, product_id, color=None):
    cart = Cart(request)
    product = get_object_or_404(ProductModel, id=product_id)

    if color is not None and color != 'None':
        cart.cart[str(product_id)]['colors'][color]['item_quantity'] += 1

        cart.cart[str(product_id)]['quantity'] = sum(
            [q_s['item_quantity'] for color, q_s in cart.cart[str(product_id)]['colors'].items()])
    else:
        cart.cart[str(product_id)]['quantity'] += 1
    cart.save()

    html = render_block_to_string('cart-detail.html',
                                  'cart-update',
                                  context={'my_cart': cart})
    return HttpResponse(html)


@require_POST
def minus_quantity(request, product_id, color=None):
    cart = Cart(request)

    product = get_object_or_404(ProductModel, id=product_id)
    print(color)
    if color is not None and color != 'None':
        cart.cart[str(product_id)]['colors'][color]['item_quantity'] -= 1

        cart.cart[str(product_id)]['quantity'] = sum(
            [q_s['item_quantity'] for color, q_s in cart.cart[str(product_id)]['colors'].items()])

        if cart.cart[str(product_id)]['colors'][color]['item_quantity'] <= 0:
            del cart.cart[str(product_id)]['colors'][color]

            cart.cart[str(product_id)]['quantity'] = sum(
                [q_s['item_quantity'] for color, q_s in cart.cart[str(product_id)]['colors'].items()])
    else:
        cart.cart[str(product_id)]['quantity'] -= 1
        if cart.cart[str(product_id)]['quantity'] <= 0:
            del cart.cart[str(product_id)]

    cart.save()

    html = render_block_to_string('cart-detail.html',
                                  'cart-update',
                                  context={'my_cart': cart})
    return HttpResponse(html)


@require_POST
def product_remove(request, product_id, color=None):
    cart = Cart(request)

    if color is not None and color != 'None':
        del cart.cart[str(product_id)]['colors'][color]
        cart.cart[str(product_id)]['quantity'] = sum(
            [q_s['item_quantity'] for color, q_s in cart.cart[str(product_id)]['colors'].items()])
    else:
        del cart.cart[str(product_id)]

    cart.save()

    html = render_block_to_string('cart-detail.html',
                                  'cart-update',
                                  context={'my_cart': cart})
    return HttpResponse(html)


@require_POST
def product_remove_navbar(request, product_id, color=None):
    cart = Cart(request)
    if color is not None and color != 'None':
        del cart.cart[str(product_id)]['colors'][color]
        cart.cart[str(product_id)]['quantity'] = sum(
            [q_s['item_quantity'] for color, q_s in cart.cart[str(product_id)]['colors'].items()])
    else:
        del cart.cart[str(product_id)]

    cart.save()

    html = render_block_to_string('layouts/navbar.html',
                                  'cart-update',
                                  context={'cart': cart})
    return HttpResponse(html)
