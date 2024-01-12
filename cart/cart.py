from decimal import Decimal
from django.conf import settings
from shop.models import ProductModel
from orders.models import PromoCodeModel


class Cart:
    """Class to handle cart"""

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        self.promo_code_id = self.session.get('promo_code_id', None)

    @property
    def has_discount(self):
        return bool(self.promo_code_id)

    @property
    def discount_number(self):
        if self.has_discount:
            discount = PromoCodeModel.objects.get(id=self.promo_code_id).discount
            return discount
        else:
            return 0

    def __iter__(self):
        """
        Iterate through the cart and get items
        """
        product_ids = self.cart.keys()
        # get product object and add to cart
        products = ProductModel.objects.filter(id__in=product_ids).select_related('class_of_product')
        cart = self.cart.copy()
        for product in products:
            for color, q_s in self.cart[str(product.id)].get('colors').items():
                if color:
                    quantity = q_s['item_quantity']
                else:
                    quantity = self.cart[str(product.id)]['quantity']
                size = q_s['item_size']
                yield product, color, quantity, size

    def __len__(self):
        """
        Count all the products in the cart(quantities). e.g: 3 eggs, 2 chickens = 5 items
        """
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product, quantity=1, color=None, size=None, override_quantity=False):
        """Add product to cart or update quantity"""
        if size is not None:
            size = size.replace('\n', '').replace(' ', '')
        else:
            size = 'default'
        product_id = str(product.id)

        if color is not None:
            color = color.replace('\n', '').replace(' ', '')

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.real_price),
                                     'colors': {str(color): {'item_quantity': 0, 'item_size': size}}
                                     }
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
            a = self.cart[product_id]['colors'].get(str(color))
            if a is not None:
                if a['item_quantity']:
                    a['item_quantity'] += 1
                    a['item_size'] = size
                else:
                    a['item_quantity'] = 1
                    a['item_size'] = size
            else:
                self.cart[product_id]['colors'][str(color)] = {'item_quantity': 1, 'item_size': size}
        self.save()

    def save(self):
        """
        Save the cart
        """
        self.session.modified = True

    def remove(self, product):
        """remove product"""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
        self.save()

    def get_total_price(self):
        """ total cart price"""
        if self.has_discount:
            discount = PromoCodeModel.objects.get(id=self.promo_code_id).discount
            return round(sum(Decimal(item['price']) * item['quantity']
                             for item in self.cart.values()) * Decimal(1 - discount / 100), 2)
        else:
            return round(sum(Decimal(item['price']) * item['quantity']
                             for item in self.cart.values()), 2)

    def get_total_price_before_discount(self):
        return round(sum(Decimal(item['price']) * item['quantity']
                         for item in self.cart.values()), 2)

    def discount_value(self):
        if self.has_discount:
            return round(sum(Decimal(item['price']) * item['quantity']
                             for item in self.cart.values()) * Decimal(self.discount_number / 100), 2)
        return None

    def clear(self):
        """
        Delete the cart from the sessions
        """
        del self.session[settings.CART_SESSION_ID]
        del self.session['promo_code_id']
        self.save()

    def __str__(self):
        return str(self.cart)
