# Generated by Django 3.2.3 on 2021-08-04 10:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20210804_1323'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gloves',
            name='rating',
        ),
    ]
