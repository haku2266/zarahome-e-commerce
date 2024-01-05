from django.db.models import Sum
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, m2m_changed
from .models import OrderModel, OrderItemModel
from decimal import Decimal

#
# @receiver(m2m_changed, sender=OrderModel.items.through)
# def count_original_real_prices(sender, action, instance, **kwargs):
#     print(instance.items.all().aggregate(Sum('price'))['price__sum'])
#     if action == 'post_add' or action == 'post_remove':
#         instance.price = round(float(instance.items.all().aggregate(Sum('price'))['price__sum']), 2)
#         if instance.has_promo_code():
#             instance.real_price = round(float(instance.price) * (1 - instance.promo_code.discount / 100), 2)
#         else:
#             instance.real_price = instance.price
#         instance.save()


# @receiver(pre_save, sender=OrderModel)
# def promo_code_update(sender, instance, **kwargs):
#     if instance.has_promo_code():
#         instance.real_price = round(float(instance.price) * (1 - instance.promo_code.discount / 100), 2)
#     else:
#         instance.real_price = instance.price


@receiver(post_save, sender=OrderItemModel)
def set_total_cost(sender, instance, created, **kwargs):
    if created:
        order_id = instance.order.id
        order = OrderModel.objects.get(id=order_id)
        my_order = order
        print(my_order.items.all())
        if my_order.has_promo_code():
            my_order.total_cost = sum(item.get_cost() for item in my_order.items.all()) * Decimal(
                        1 - my_order.promo_code.discount / 100)
        else:
            my_order.total_cost = sum(item.get_cost() for item in my_order.items.all())
        my_order.save()
