from django.shortcuts import render, redirect
from cart.cart import Cart
from .models import OrderItemModel
from .forms import OrderAddressCreateForm


def get_orders(request):
    pass


def create_order(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderAddressCreateForm(request.POST)
        if form.is_valid():

            form.cleaned_data['uuid'] = str(request.user.pk)

            order = form.save()
            for product, quantity in cart:
                OrderItemModel.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=product.real_price)
            cart.clear()
            return redirect('shop:home')
    else:
        form = OrderAddressCreateForm()
    return render(request, 'create-order.html',
                  context={'form': form,
                           'cart': cart})
