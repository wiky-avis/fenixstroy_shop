from django.contrib import admin

from .models import Article, ArticleComment, Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    list_display_links = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    empty_value_display = '-пусто-'


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'slug', 'pub_date', 'category', 'published')
    list_display_links = ('title',)
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    empty_value_display = '-пусто-'


class ArticleCommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'article', 'text', 'created')
    list_display_links = ('author',)
    search_fields = ('article',)
    empty_value_display = '-пусто-'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleComment, ArticleCommentAdmin)
