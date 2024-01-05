from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import ClientDetails
from shop.models import ProductModel


class PromoCodeModel(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name=_('promo code'),
                            help_text=_('promo code that would give discount for an order'))
    discount = models.PositiveSmallIntegerField(default=0, verbose_name=_('discount'),
                                                help_text=_('discount issued by the promo code'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    expire_at = models.DateTimeField(null=True, blank=True, verbose_name=_('expire date'))

    def __str__(self):
        return f'promo: {self.code}'

    class Meta:
        db_table = 'promo_code'
        verbose_name = _('promo code')
        verbose_name_plural = _('promo codes')
        ordering = ('-created_at',)


class OrderModel(models.Model):
    client = models.ForeignKey(ClientDetails, on_delete=models.SET_NULL, null=True,
                               verbose_name=_('client'))
    promo_code = models.ForeignKey(PromoCodeModel, on_delete=models.SET_NULL, null=True, blank=True,
                                   verbose_name=_('promo code'),
                                   help_text=_('promo code that would give discount for an order'))

    CHOICES = (('waiting', 'waiting for payment'),
               ('preparing', 'preparing for delivery'),
               ('done', 'done'))

    total_cost = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=99)

    status = models.CharField(max_length=20, choices=CHOICES, default='waiting',
                              verbose_name=_('status'), help_text=_('status of the order'))

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'order #{self.id} by {self.client}'

    def has_promo_code(self):
        return bool(self.promo_code)

    def get_total_cost(self):
        if self.has_promo_code():
            return sum(item.get_cost() for item in self.items.all()) * (1 - self.promo_code.discount / 100)
        else:
            return sum(item.get_cost() for item in self.items.all())

    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')
        ordering = ('-created_at',)
        db_table = 'order'


class OrderItemModel(models.Model):
    order = models.ForeignKey(OrderModel,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel,
                                related_name='order_items',
                                on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=10,
                                decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity

    class Meta:
        verbose_name = _('order item')
        verbose_name_plural = _('order items')
        db_table = 'order_item'
