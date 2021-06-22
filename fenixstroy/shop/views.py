from django.shortcuts import render, get_object_or_404, redirect
from .models import Cart, Gloves, Category, LatestProducts, Product
from django.views.generic.base import View
from .mixins import CategoryDetailMixin, CartMixin
from django.db.models import Avg
from django.contrib.contenttypes.models import ContentType
from .utils import recalc_cart
from django.contrib import messages
from django.http import HttpResponseRedirect
from .forms import OrderForm
from django.db import transaction

from django.views.generic import DetailView
from django.contrib.auth import get_user_model

User = get_user_model()


class BaseView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.filter(published=True).all()
        products = LatestProducts.objects.get_products_for_main_page(
            'gloves',
            whith_respect_to='gloves')
        return render(
            request, 'base.html', {
                'categories': categories, 'products': products, 'cart': self.cart})


class ShopView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.filter(published=True).all()
        products = Gloves.objects.filter(published=True).all()
        return render(
            request, 'shop.html', {
                'categories': categories, 'products': products, 'cart': self.cart})


class ProductDetailView(CartMixin, CategoryDetailMixin, DetailView):
    model = Gloves
    queryset = Gloves.objects.filter(published=True).all()
    context_object_name = 'product'
    template_name = 'product_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        gloves = get_object_or_404(Gloves, slug=self.kwargs.get('slug'))
        int_rating = gloves.comments.all().aggregate(Avg('score'))
        context['int_rating'] = int_rating['score__avg']
        context['cart'] = self.cart
        return context


class CategoryDetailView(CartMixin, CategoryDetailMixin, DetailView):
    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'category_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        return context
