# Generated by Django 3.2.3 on 2021-08-04 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.CharField(max_length=100, verbose_name='Автор'),
        ),
    ]
