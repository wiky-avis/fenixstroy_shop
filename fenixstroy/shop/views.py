from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView
from django.views.generic.base import View

from cart.forms import CartAddProductForm

from .mixins import CategoryDetailMixin
from .models import Category, Gloves, LatestProducts

User = get_user_model()


class BaseView(View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.filter(published=True).all()
        products = LatestProducts.objects.get_products_for_main_page(
            'gloves',
            whith_respect_to='gloves')
        return render(
            request, 'base.html', {
                'categories': categories, 'products': products})


class ShopView(View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.filter(published=True).all()
        products = Gloves.objects.filter(published=True).all()
        return render(
            request, 'shop.html', {
                'categories': categories, 'products': products})


class ProductDetailView(CategoryDetailMixin, DetailView):
    model = Gloves
    queryset = Gloves.objects.filter(published=True).all()
    context_object_name = 'product'
    template_name = 'product_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        gloves = get_object_or_404(
            Gloves, pk=self.kwargs.get('id'), slug=self.kwargs.get('slug')
            )
        int_rating = gloves.comments.all().aggregate(Avg('score'))
        context['int_rating'] = int_rating['score__avg']
        context['cart_product_form'] = CartAddProductForm()
        return context


class CategoryDetailView(CategoryDetailMixin, DetailView):
    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'category_detail.html'
    slug_url_kwarg = 'category_slug'

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        category = get_object_or_404(
            Category, slug=self.kwargs.get('category_slug')
            )
        context['products'] = category.category_products.all()
        return context
