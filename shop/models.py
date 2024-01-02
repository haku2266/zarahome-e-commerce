from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from users.models import CustomUserModel


class CategoryModel(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name=_('category'), help_text=_('name of category'))
    slug = models.SlugField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product_category'
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ('-created_at',)

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            slug = slugify(self.name)
            slug_exists = True
            counter = 1
            self.slug = slug
            while slug_exists:
                try:
                    slug_exits = CategoryModel.objects.get(slug=slug)
                    if slug_exits:
                        slug = self.slug + '-' + str(counter)
                        counter += 1
                except CategoryModel.DoesNotExist:
                    self.slug = slug
                    break
        return super().save(*args, **kwargs)


class ColorModel(models.Model):
    code = models.CharField(max_length=50, verbose_name=_('color code'), help_text=_('color code'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))

    def __str__(self):
        return self.code

    class Meta:
        db_table = 'color'
        verbose_name = _('color code')
        verbose_name_plural = _('color codes')


class SizeModel(models.Model):
    size = models.CharField(max_length=50, verbose_name=_('size'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))

    def __str__(self):
        return self.size

    class Meta:
        db_table = 'product_size'
        verbose_name = _('size')
        verbose_name_plural = _('sizes')


class TypeModel(models.Model):
    name = models.CharField(max_length=60, unique=True, verbose_name=_('type'), help_text=_('type of product'))
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE, related_name='types',
                                 verbose_name=_('category of type'), help_text=_('category'))
    slug = models.SlugField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))

    def __str__(self):
        return f'{self.name}, category: {self.category}'

    class Meta:
        db_table = 'product_type'
        verbose_name = _('type')
        verbose_name_plural = _('type')
        ordering = ('-created_at',)

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            slug = slugify(self.name)
            slug_exists = True
            counter = 1
            self.slug = slug
            while slug_exists:
                try:
                    slug_exits = TypeModel.objects.get(slug=slug)
                    if slug_exits:
                        slug = self.slug + '-' + str(counter)
                        counter += 1
                except TypeModel.DoesNotExist:
                    self.slug = slug
                    break
        return super().save(*args, **kwargs)


class ProductClassModel(models.Model):
    name = models.CharField(max_length=60, unique=True, verbose_name=_('class'))
    type = models.ForeignKey(TypeModel, on_delete=models.CASCADE, related_name='classes')
    slug = models.SlugField(unique=True, null=True, blank=True, verbose_name=_('slug'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))

    def __str__(self):
        return f'class: {self.name}, type: {self.type}'

    class Meta:
        db_table = 'product_class'
        verbose_name = _('product class')
        verbose_name_plural = _('product classes')
        ordering = ('-created_at',)

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            slug = slugify(self.name)
            slug_exists = True
            counter = 1
            self.slug = slug
            while slug_exists:
                try:
                    slug_exits = ProductClassModel.objects.get(slug=slug)
                    if slug_exits:
                        slug = self.slug + '-' + str(counter)
                        counter += 1
                except ProductClassModel.DoesNotExist:
                    self.slug = slug
                    break
        return super().save(*args, **kwargs)


class ProductModel(models.Model):
    def dynamic_directory(self, filename):
        return f'products/{self.slug}/{self.name}/{filename}'

    class_of_product = models.ForeignKey(ProductClassModel, on_delete=models.SET_NULL,
                                         related_name='products', null=True, blank=True)
    sizes = models.ManyToManyField(SizeModel, related_name='products', verbose_name=_('size'))

    colors = models.ManyToManyField(ColorModel, related_name='products')

    name = models.CharField(max_length=60, verbose_name=_('name'), help_text=_('name of product [max 60 characters]'))
    slug = models.SlugField(null=True, blank=True)
    description = models.TextField(verbose_name=_('description'), blank=True, null=True,
                                   help_text=_('description of product'))
    image = models.ImageField(upload_to=dynamic_directory, null=True, blank=True)

    sale = models.BooleanField(verbose_name=_('sale'), default=False, help_text=_('is the product on sale'))

    price = models.DecimalField(decimal_places=2, verbose_name=_('price'), default=0, max_digits=100, blank=True, null=True,
                                help_text=_('original price of product. at most 2 decimals. f.e: 1234,56'))
    discount = models.PositiveSmallIntegerField(default=0, verbose_name=_('discount'),
                                                help_text=_('discount percentage of product. [1-100]'))
    real_price = models.DecimalField(verbose_name=_('real price'), max_digits=100, decimal_places=2, null=True,
                                     blank=True, help_text=_('price of product after discount'))

    delivery_duration = models.DurationField(blank=True, null=True, verbose_name=_('delivery duration'),
                                             help_text=_('how long will it take to deliver'))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))

    def is_discount(self):
        return bool(self.discount)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = 'product'
        verbose_name = _('product')
        verbose_name_plural = _('products')

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            slug = slugify(self.name)
            slug_exists = True
            counter = 1
            self.slug = slug
            while slug_exists:
                try:
                    slug_exits = ProductModel.objects.get(slug=slug)
                    if slug_exits:
                        slug = self.slug + '-' + str(counter)
                        counter += 1
                except ProductModel.DoesNotExist:
                    self.slug = slug
                    break
        return super().save(*args, **kwargs)


class CartModel(models.Model):
    user = models.OneToOneField(CustomUserModel, on_delete=models.CASCADE, verbose_name=_('user'), related_name='cart')

    def __str__(self):
        return f'cart of {self.user}'

    class Meta:
        db_table = 'cart'
        verbose_name = _('cart')
        verbose_name_plural = _('carts')


class CartItemModel(models.Model):
    cart = models.ForeignKey(CartModel, on_delete=models.CASCADE, verbose_name=_('cart'), related_name='items')
    product = models.OneToOneField(ProductModel, on_delete=models.CASCADE,
                                   related_name='cart_item',
                                   verbose_name=_('cart item'))
    quantity = models.PositiveIntegerField(default=1, verbose_name=_('quantity'))
    price = models.DecimalField(max_digits=100, decimal_places=2, verbose_name=_('price'), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'cart-item: {self.product} x {self.quantity}'

    class Meta:
        db_table = 'cart_item'
        verbose_name = _('cart item')
        verbose_name_plural = _('cart items')
