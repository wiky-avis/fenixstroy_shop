from django.contrib.auth import get_user_model
from django.views.generic.detail import SingleObjectMixin

from cart.forms import CartAddProductForm

from .models import Category, Manufacturer

User = get_user_model()


class CategoryDetailMixin(SingleObjectMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(published=True).all()
        return context


class CartAddProductFormMixin(SingleObjectMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_product_form'] = CartAddProductForm()
        return context


class ManufacturerMixin(SingleObjectMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['manufacturer'] = Manufacturer.objects.all()
        return context


class MyGlovesMixins(
    CategoryDetailMixin, CartAddProductFormMixin, ManufacturerMixin
    ):
    pass
