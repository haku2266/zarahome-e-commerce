from django import forms
from django.utils.safestring import mark_safe


# PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 99)]


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={'class': "text-center", 'value': "1",
                                                                  'style': "border: 1px solid rgba(0, 0, 0, 0.25);"
                                                                           " background:  # FFF;"
                                                                  }))
    override = forms.BooleanField(required=False,
                                  initial=False,
                                  widget=forms.HiddenInput)
