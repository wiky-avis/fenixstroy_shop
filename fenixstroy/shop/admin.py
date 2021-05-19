from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import (Cart, CartProduct, Category, CustomUser, Gloves,
                     Manufacturer)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug', 'published')
    list_display_links = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['published']
    empty_value_display = '-пусто-'


class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    list_display_links = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    empty_value_display = '-пусто-'


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'phone', 'address')
    list_display_links = ('user',)
    search_fields = ('user',)
    empty_value_display = '-пусто-'


class GlovesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'article_number', 'name', 'price', 'category', 'manufacturer', 'published')
    list_display_links = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    empty_value_display = '-пусто-'
    # readonly_fields = ('get_image',)
    list_editable = ['category', 'price', 'manufacturer', 'published']

    # def get_image(self, obj):
    #     return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    # get_image.short_description = 'Изображение товара'


class CartProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'cart')
    list_display_links = ('pk',)
    empty_value_display = '-пусто-'


class CartAdmin(admin.ModelAdmin):
    list_display = ('pk', 'owner', 'total_products', 'final_price')
    list_display_links = ('pk',)
    empty_value_display = '-пусто-'


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(CartProduct, CartProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Gloves, GlovesAdmin)
