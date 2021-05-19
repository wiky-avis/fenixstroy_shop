from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse

User = get_user_model()


class CustomUser(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Пользователь')
    phone = models.CharField(max_length=20, verbose_name='Номер телефона')
    address = models.CharField(
        max_length=255, verbose_name='Адрес доставки', null=True, blank=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('user__username',)

    def __str__(self) -> str:
        return f'Пользователь: {self.user.last_name} {self.user.first_name}'


class Category(models.Model):
    name = models.CharField(max_length=70, verbose_name='Название категории')
    slug = models.SlugField(verbose_name='Псевдоним', unique=True)
    published = models.BooleanField(verbose_name='Опубликовано')

    class Meta:
        verbose_name_plural = 'Категории'
        verbose_name = 'Категория'
        ordering = ('name',)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])


class Manufacturer(models.Model):
    name = models.CharField(max_length=70, verbose_name='Производитель')
    slug = models.SlugField(verbose_name='Псевдоним', unique=True)

    class Meta:
        verbose_name_plural = 'Производители'
        verbose_name = 'Производитель'
        ordering = ('name',)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название товара')
    slug = models.SlugField(unique=True, verbose_name='Псевдоним')
    article_number = models.CharField(
        max_length=20, verbose_name='Артикул', null=True, blank=True)
    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.SET_NULL,
        verbose_name='Производитель',
        null=True,
        blank=True,
        related_name='manufacturer_products')
    desctriptions = models.TextField(
        verbose_name='Описание товара', null=True, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория товара',
        related_name='category_products',
        null=True)
    price = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        verbose_name='Цена товара, руб.',
        null=True,
        blank=True)
    image = models.ImageField(
        verbose_name='Изображение товара',
        upload_to='products/',
        null=True,
        blank=True)
    published = models.BooleanField(verbose_name='Опубликовано')

    class Meta:
        verbose_name_plural = 'Товары'
        verbose_name = 'Товар'
        ordering = ('price', 'name')
        abstract = True

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])


class CartProduct(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, verbose_name='Покупатель')
    cart = models.ForeignKey(
        'Cart',
        on_delete=models.CASCADE,
        related_name='cart_products',
        verbose_name='Корзина')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_obj = GenericForeignKey('content_type', 'object_id')
    total_products = models.PositiveIntegerField(
        default=1, verbose_name='Количество')
    final_price = models.DecimalField(
        max_digits=9, decimal_places=2, verbose_name='Общая цена')

    class Meta:
        verbose_name_plural = 'Товары корзины'
        verbose_name = 'Товар корзины'

    def __str__(self) -> str:
        return f'Продукт: {self.product.title}(для корзины).'


class Cart(models.Model):
    owner = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, verbose_name='Владелец')
    products = models.ManyToManyField(
        CartProduct, related_name='related_cart', blank=True)
    total_products = models.PositiveIntegerField(
        default=0, verbose_name='Количество')
    final_price = models.DecimalField(
        max_digits=9, decimal_places=2, verbose_name='Общая цена')

    class Meta:
        verbose_name_plural = 'Корзины'
        verbose_name = 'Корзина'

    def __str__(self) -> str:
        return self.id


class Gloves(Product):
    features = models.CharField(
        max_length=255, verbose_name='свойства товара', null=True, blank=True)
    material = models.CharField(
        max_length=70, verbose_name='материал основы', null=True, blank=True)
    coating_material = models.CharField(
        max_length=70, verbose_name='материал покрытия', null=True, blank=True)
    type_coating = models.CharField(
        max_length=70, verbose_name='тип покрытия', null=True, blank=True)
    color = models.CharField(
        max_length=150, verbose_name='цвет', null=True, blank=True)
    size = models.CharField(
        max_length=150, verbose_name='размер', null=True, blank=True)
    quantity_pack = models.CharField(
        max_length=10,
        verbose_name='количество в упаковке',
        null=True,
        blank=True)
    minimum_packaging = models.CharField(
        max_length=10,
        verbose_name='минимальная упаковка',
        null=True,
        blank=True)
    pair_weight = models.CharField(
        max_length=10, verbose_name='вес пары', null=True, blank=True)

    def __str__(self):
        return f'{self.category.name} {self.name}'
