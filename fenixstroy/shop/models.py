from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
import sys
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.contrib.auth.models import AbstractUser



def get_product_url(obj, viewname):
    """для формирования слага"""
    # ct_model = obj.__class__._meta.model_name
    # return reverse(viewname, kwargs={'ct-model': ct_model, 'slug': obj.slug})
    return reverse(viewname, kwargs={'slug': obj.slug})


class MinResolutionErrorException(Exception):
    pass


class MaxResolutionErrorException(Exception):
    pass


class LatestProductManager:

    @staticmethod
    def get_products_for_main_page(*args, **kwargs):
        with_respect_to = kwargs.get('with_respect_to')
        products = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_products = (
                ct_model.model_class()._base_manager.all().order_by('-id')[:5])
            products.extend(model_products)
        if with_respect_to:
            ct_model = ContentType.objects.filter(model=with_respect_to)
            if ct_model.exists():
                if with_respect_to in args:
                    return sorted(
                        products,
                        key=lambda x: x.__class__._meta.model_name.startswith(
                            with_respect_to),
                        reverse=True
                    )
        return products


class LatestProducts:

    objects = LatestProductManager()


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20, verbose_name='Номер телефона')
    address = models.CharField(
        max_length=255, verbose_name='Адрес доставки', null=True, blank=True)

    orders = models.ManyToManyField('Order', verbose_name='Заказы покупателя', related_name='related_order')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self) -> str:
        return f'Пользователь: {self.last_name} {self.first_name}'


class Category(models.Model):
    name = models.CharField(max_length=70, verbose_name='Название категории')
    slug = models.SlugField(verbose_name='Псевдоним', unique=True)
    published = models.BooleanField(verbose_name='Опубликовано')
    image = models.ImageField(
        verbose_name='Изображение товара',
        upload_to='categories/',
        null=True,
        blank=True)

    class Meta:
        verbose_name_plural = 'Категории'
        verbose_name = 'Категория'
        ordering = ('name',)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


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
    MIN_RESOLUTION = (400, 400)

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
    rating = models.IntegerField(
        'Рейтинг', null=True, blank=True, default=0)
    published = models.BooleanField(verbose_name='Опубликовано')

    class Meta:
        verbose_name_plural = 'Товары'
        verbose_name = 'Товар'
        ordering = ('price', 'name')
        abstract = True

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return get_product_url('product_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        image = self.image
        img = Image.open(image)

        min_height, min_width = self.MIN_RESOLUTION
        if img.height < min_height or img.width < min_width:
            raise MinResolutionErrorException(
                'Разрешение изображения меньше минимального 400х400!')

        new_img = img.convert('RGB')
        resized_new_img = new_img.resize((800, 800), Image.ANTIALIAS)
        filestream = BytesIO()
        resized_new_img.save(filestream, 'JPEG', quality=90)
        filestream.seek(0)
        name = '{}.{}'.format(*self.image.name.split('.'))
        self.image = InMemoryUploadedFile(
            filestream,
            'ImageField',
            name,
            'jpeg/image',
            sys.getsizeof(filestream),
            None
        )

        super().save(*args, **kwargs)


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

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class Gallery(models.Model):
    image = models.ImageField(
        verbose_name='Изображение товара',
        upload_to='gallery/',
        null=True,
        blank=True)
    gloves = models.ForeignKey(
        Gloves, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return f'{self.image.url}'

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class Comment(models.Model):
    product = models.ForeignKey(
        Gloves,
        on_delete=models.CASCADE,
        related_name='comments', verbose_name='Товар')
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='comments', verbose_name='Автор')
    text = models.TextField(
        verbose_name='Комментарий',
        help_text='Введите пожалуйста текст вашего комментария')
    score = models.IntegerField(
        'Оценка',
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    created = models.DateTimeField(
        verbose_name='Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
