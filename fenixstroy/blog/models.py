from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=70, verbose_name='Название категории')
    slug = models.SlugField(verbose_name='Слаг')

    class Meta:
        ordering = ('-name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.name


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
    published = models.BooleanField(verbose_name='Опубликовано')
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='articles/',
        null=True,
        blank=True, default='default/def.jpg',)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse('blog:blog_detail', kwargs={'slug': self.slug})


class ArticleComment(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='article_comments', verbose_name='Статья')
    author = models.CharField(max_length=150)
    text = models.TextField(
        verbose_name='Комментарий',
        help_text='Введите пожалуйста текст вашего комментария')
    created = models.DateTimeField(
        verbose_name='Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self) -> str:
        return f'Комментарий к статье {self.article.id}'
