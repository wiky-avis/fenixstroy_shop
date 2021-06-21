# Generated by Django 3.2.3 on 2021-06-21 17:12

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('phone', models.CharField(max_length=20, verbose_name='Номер телефона')),
                ('address', models.CharField(blank=True, max_length=255, null=True, verbose_name='Адрес доставки')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
                'ordering': ('username',),
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70, verbose_name='Название категории')),
                ('slug', models.SlugField(unique=True, verbose_name='Псевдоним')),
                ('published', models.BooleanField(verbose_name='Опубликовано')),
                ('image', models.ImageField(blank=True, null=True, upload_to='categories/', verbose_name='Изображение товара')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70, verbose_name='Производитель')),
                ('slug', models.SlugField(unique=True, verbose_name='Псевдоним')),
            ],
            options={
                'verbose_name': 'Производитель',
                'verbose_name_plural': 'Производители',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Gloves',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название товара')),
                ('slug', models.SlugField(unique=True, verbose_name='Псевдоним')),
                ('article_number', models.CharField(blank=True, max_length=20, null=True, verbose_name='Артикул')),
                ('desctriptions', models.TextField(blank=True, null=True, verbose_name='Описание товара')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True, verbose_name='Цена товара, руб.')),
                ('image', models.ImageField(blank=True, null=True, upload_to='products/', verbose_name='Изображение товара')),
                ('rating', models.IntegerField(blank=True, default=0, null=True, verbose_name='Рейтинг')),
                ('published', models.BooleanField(verbose_name='Опубликовано')),
                ('features', models.CharField(blank=True, max_length=255, null=True, verbose_name='свойства товара')),
                ('material', models.CharField(blank=True, max_length=70, null=True, verbose_name='материал основы')),
                ('coating_material', models.CharField(blank=True, max_length=70, null=True, verbose_name='материал покрытия')),
                ('type_coating', models.CharField(blank=True, max_length=70, null=True, verbose_name='тип покрытия')),
                ('color', models.CharField(blank=True, max_length=150, null=True, verbose_name='цвет')),
                ('size', models.CharField(blank=True, max_length=150, null=True, verbose_name='размер')),
                ('quantity_pack', models.CharField(blank=True, max_length=10, null=True, verbose_name='количество в упаковке')),
                ('minimum_packaging', models.CharField(blank=True, max_length=10, null=True, verbose_name='минимальная упаковка')),
                ('pair_weight', models.CharField(blank=True, max_length=10, null=True, verbose_name='вес пары')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category_products', to='shop.category', verbose_name='Категория товара')),
                ('manufacturer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='manufacturer_products', to='shop.manufacturer', verbose_name='Производитель')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
                'ordering': ('price', 'name'),
                'abstract': False,
                'index_together': {('id', 'slug')},
            },
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='gallery/', verbose_name='Изображение товара')),
                ('gloves', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='shop.gloves')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(help_text='Введите пожалуйста текст вашего комментария', verbose_name='Комментарий')),
                ('score', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Оценка')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='shop.gloves', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
                'ordering': ('-created',),
            },
        ),
    ]
