from decimal import Decimal
from django.conf import settings
from shop.models import ProductModel


class Cart:
    """Class to handle cart"""

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, color=None, override_quantity=False):
        """Add product to cart or update quantity"""

        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.real_price),
                                     'colors': {str(color): {'item_quantity': 0, 'item_size': None}}
                                     }
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
            a = self.cart[product_id]['colors'].get(str(color))
            if a is not None:
                if a['item_quantity']:
                    a['item_quantity'] += 1
                else:
                    a['item_quantity'] = 1
            else:
                self.cart[product_id]['colors'][str(color)] = {'item_quantity': 1, 'item_size': None}
        self.save()

    def save(self):
        """
        Save the cart
        """
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
        self.save()

    def __iter__(self):
        """
        Iterate through the cart and get items
        """
        product_ids = self.cart.keys()
        # get product object and add to cart
        products = ProductModel.objects.filter(id__in=product_ids).select_related('class_of_product')
        cart = self.cart.copy()
        for product in products:
            quantity = self.cart[str(product.id)]['quantity']
            yield product, quantity
        #     cart[str(product.id)]['product'] = product
        # for item in cart.values():
        #     item['price'] = Decimal(item['price'])
        #     item['total_price'] = item['price'] * item['quantity']
        #     yield item

    def __len__(self):
        """
        Count all the products in the cart(quantities). e.g: 3 eggs, 2 chickens = 5 items
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity']
                   for item in self.cart.values())

    def clear(self):
        """
        Delete the cart from the sessions
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def __str__(self):
        return str(self.cart)
