from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import ClientDetails
from shop.models import CartItemModel


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
    items = models.ManyToManyField(CartItemModel, related_name='orders', verbose_name=_('items'),
                                   help_text=_('Items related to the order'))
    promo_code = models.ForeignKey(PromoCodeModel, on_delete=models.SET_NULL, null=True, blank=True,
                                   verbose_name=_('promo code'),
                                   help_text=_('promo code that would give discount for an order'))
    price = models.DecimalField(max_digits=100, decimal_places=2, null=True, blank=True,
                                verbose_name=_('total price'), help_text=_('total price of the order'))
    real_price = models.DecimalField(max_digits=100, decimal_places=2, null=True, blank=True,
                                     verbose_name=_('real price'),
                                     help_text=_('price of the order with promo-code'))

    CHOICES = (('waiting', 'waiting for payment'),
               ('preparing', 'preparing for delivery'),
               ('done', 'done'))

    status = models.CharField(max_length=20, choices=CHOICES, default='waiting',
                              verbose_name=_('status'), help_text=_('status of the order'))

    created_at = models.DateTimeField(auto_now_add=True)

    def has_promo_code(self):
        return bool(self.promo_code)

    def __str__(self):
        return f'order #{self.id} by {self.client}'

    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')
        ordering = ('-created_at',)
        db_table = 'order'
