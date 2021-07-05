# Generated by Django 3.2.3 on 2021-07-05 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, default='default/def.jpg', null=True, upload_to='categories/', verbose_name='Изображение товара'),
        ),
        migrations.AlterField(
            model_name='gallery',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='products/gallery/', verbose_name='Изображение товара'),
        ),
        migrations.AlterField(
            model_name='gloves',
            name='image',
            field=models.ImageField(blank=True, default='default/def.jpg', null=True, upload_to='products/', verbose_name='Изображение товара'),
        ),
    ]