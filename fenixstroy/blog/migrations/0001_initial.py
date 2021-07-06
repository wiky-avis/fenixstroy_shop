# Generated by Django 3.2.3 on 2021-07-06 13:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Статья')),
                ('slug', models.SlugField(verbose_name='Слаг')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('text', models.TextField(verbose_name='Текст поста')),
                ('published', models.BooleanField(verbose_name='Опубликовано')),
            ],
            options={
                'verbose_name': 'Статья',
                'verbose_name_plural': 'Статьи',
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70, verbose_name='Название категории')),
                ('slug', models.SlugField(verbose_name='Слаг')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ('-name',),
            },
        ),
        migrations.CreateModel(
            name='ArticleComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(help_text='Введите пожалуйста текст вашего комментария', verbose_name='Комментарий')),
                ('image', models.ImageField(blank=True, default='default/def.jpg', null=True, upload_to='articles/', verbose_name='Изображение')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article_comments', to='blog.article', verbose_name='Статья')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
                'ordering': ('-created',),
            },
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.category', verbose_name='Категория'),
        ),
    ]
