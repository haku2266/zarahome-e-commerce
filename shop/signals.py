from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from .models import ProductModel
from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(pre_save, sender=ProductModel)
def real_price_product(sender, instance, **kwargs):
    if instance.is_discount():
        instance.real_price = round((1 - instance.discount / 100) * float(instance.price), 2)
    else:
        instance.real_price = instance.price


@receiver(pre_save, sender=ProductModel)
def set_sale(sender, instance, *args, **kwargs):
    if instance.is_discount():
        instance.sale = True
    else:
        instance.sale = False
