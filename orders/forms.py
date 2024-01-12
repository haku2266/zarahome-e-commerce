from django import forms
from .models import OrderModel, OrderItemModel, PromoCodeModel
from users.models import ClientDetails, CustomUserModel


class OrderAddressCreateForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    region = forms.CharField()
    city = forms.CharField()
    street = forms.CharField()
    flat_number = forms.IntegerField()
    user_uuid = forms.CharField(required=False, widget=forms.HiddenInput(attrs={'class': 'form-control'}))

    class Meta:
        model = OrderModel
        fields = ['promo_code', 'discount']
        widgets = {
            'discount': forms.HiddenInput(),
            'promo_code': forms.TextInput(attrs={
                'hx-post': "/orders/promo_check/",
                'hx-trigger': "keyup",
                'hx-target': "#temp_update"
            })
        }

    def __init__(self, *args, **kwargs):
        super(OrderAddressCreateForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        order_instance = super(OrderAddressCreateForm, self).save(commit=False)
        user = CustomUserModel.objects.get(uuid=self.cleaned_data['uuid'])
        client = ClientDetails.objects.create(user=user,
                                              first_name=self.cleaned_data['first_name'],
                                              last_name=self.cleaned_data['last_name'],
                                              region=self.cleaned_data['region'],
                                              city=self.cleaned_data['city'],
                                              street=self.cleaned_data['street'],
                                              flat_number=self.cleaned_data['flat_number'])
        order_instance.client = client

        if commit:
            order_instance.save()
        return order_instance


class ColorModelAdminForms(forms.ModelForm):
    code = forms.CharField(widget=forms.TextInput(attrs={'type': 'color'}))

    class Meta:
        model = OrderItemModel
        fields = '__all__'
