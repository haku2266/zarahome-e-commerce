from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from cart.cart import Cart
from .models import OrderItemModel
from .forms import OrderAddressCreateForm


def get_orders(request):
    pass


@login_required
def create_order(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderAddressCreateForm(request.POST)
        if form.is_valid():

            form.cleaned_data['uuid'] = str(request.user.pk)
            order = form.save()
            for product, color, quantity, size in cart:
                print(color)
                print(quantity)
                OrderItemModel.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=product.real_price,
                    code=color,
                    size=size)
            cart.clear()
            return redirect('shop:home')
    else:
        form = OrderAddressCreateForm()
    return render(request, 'create-order.html',
                  context={'form': form,
                           'cart': cart})
