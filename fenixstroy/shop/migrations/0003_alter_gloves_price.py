# Generated by Django 3.2.3 on 2021-05-19 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20210519_1443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gloves',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True, verbose_name='Цена товара, руб.'),
        ),
    ]
