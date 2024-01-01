from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from .models import ProductModel, CartItemModel
from django.utils.text import slugify


@receiver(post_save, sender=ProductModel)
def create_cart_item(sender, instance, created, **kwargs):
    if created:
        obj = CartItemModel.objects.create(product=instance, price=instance.real_price)


@receiver(pre_save, sender=ProductModel)
def real_price_product(sender, instance, **kwargs):
    if instance.is_discount():
        instance.real_price = round((1 - instance.discount / 100) * float(instance.price), 2)


@receiver(pre_save, sender=CartItemModel)
def cart_item_price(sender, instance, **kwargs):
    instance.price = round((instance.product.real_price * instance.quantity), 2)
