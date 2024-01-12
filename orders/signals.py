from django.db.models import Sum
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, m2m_changed
from .models import OrderModel, OrderItemModel
from decimal import Decimal


@receiver(post_save, sender=OrderItemModel)
def set_total_cost(sender, instance, created, **kwargs):
    if created:
        order_id = instance.order.id
        order = OrderModel.objects.get(id=order_id)
        my_order = order
        print(my_order.items.all())
        if my_order.has_promo_code():
            my_order.total_cost = sum(item.get_cost() for item in my_order.items.all()) * Decimal(
                        1 - my_order.discount / 100)
        else:
            my_order.total_cost = sum(item.get_cost() for item in my_order.items.all())
        my_order.save()
