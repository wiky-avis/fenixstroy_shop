from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=70, verbose_name='Название категории')
    slug = models.SlugField(verbose_name='Слаг')

    class Meta:
        ordering = ('-name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Article(models.Model):
    title = models.CharField(max_length=150, verbose_name='Статья')
    slug = models.SlugField(verbose_name='Слаг')
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации')
    text = models.TextField(verbose_name='Текст поста')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        null=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class ArticleComment(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='article_comments', verbose_name='Статья')
    text = models.TextField(
        verbose_name='Комментарий',
        help_text='Введите пожалуйста текст вашего комментария')
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='articles/',
        null=True,
        blank=True, default='default/def.jpg',)
    created = models.DateTimeField(
        verbose_name='Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
