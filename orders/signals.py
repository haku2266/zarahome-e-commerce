from django.db.models import Sum
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, m2m_changed
from .models import OrderModel


@receiver(m2m_changed, sender=OrderModel.items.through)
def count_original_real_prices(sender, action, instance, **kwargs):
    print(instance.items.all().aggregate(Sum('price'))['price__sum'])
    if action == 'post_add' or action == 'post_remove':
        instance.price = round(float(instance.items.all().aggregate(Sum('price'))['price__sum']), 2)
        instance.real_price = round(instance.price * (1-instance.promo_code.discount/100), 2)
        instance.save()

