from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from cart.cart import Cart
from .models import OrderItemModel, PromoCodeModel
from .forms import OrderAddressCreateForm
from django.utils import timezone
from render_block import render_block_to_string


def get_orders(request):
    pass


@login_required
def create_order(request):
    cart = Cart(request)
    print(cart.discount_number)
    if request.method == 'POST':
        form = OrderAddressCreateForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.cleaned_data['uuid'] = str(request.user.pk)
            order = form.save(commit=False)
            order.discount = int(cart.discount_number)
            try:
                code = PromoCodeModel.objects.get(code=form.cleaned_data['promo_code'], expire_at__gte=timezone.now())
                code_name = code.code
            except PromoCodeModel.DoesNotExist:
                code_name = None
            order.promo_code = code_name
            order.save()
            print(order)
            for product, color, quantity, size in cart:
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


@login_required
def check_promo(request):
    data = request.POST.get('promo_code')
    try:
        promo_code = PromoCodeModel.objects.get(code=data, expire_at__gte=timezone.now())
        request.session['promo_code_id'] = promo_code.id
    except PromoCodeModel.DoesNotExist:
        request.session['promo_code_id'] = None
    cart = Cart(request)
    print(cart)
    html = render_block_to_string('create-order.html', 'temp_update', context={'cart': cart})
    return HttpResponse(html)
