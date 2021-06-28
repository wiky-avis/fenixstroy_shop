from cart.cart import Cart
from cart.forms import CartAddProductForm
from django.contrib.auth import get_user_model
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin

from .models import Category

User = get_user_model()


class CategoryDetailMixin(SingleObjectMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(published=True).all()
        return context


class CartDetailMixin(SingleObjectMixin):

    def get_context_data(self, request, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(request)
        for item in cart:
            item['update_quantity_form'] = CartAddProductForm(
                initial={'quantity': item['quantity'], 'update': True}
                )
        context['cart'] = cart
        return context
