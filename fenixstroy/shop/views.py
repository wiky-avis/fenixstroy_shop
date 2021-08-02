from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.db.models import Avg
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView
from django.views.generic.base import View
from django.views.generic.edit import CreateView

from blog.models import Article
from cart.forms import CartAddProductForm

from .mixins import CategoryDetailMixin
from .models import Category, Gloves, LatestProducts, Manufacturer, Comment

User = get_user_model()


class BaseView(View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.filter(published=True).all()
        products = LatestProducts.objects.get_products_for_main_page(
            'gloves',
            whith_respect_to='gloves')
        articles = Article.objects.all()
        cart_product_form = CartAddProductForm()
        return render(
            request, 'base.html', {
                'categories': categories,
                'products': products,
                'cart_product_form': cart_product_form,
                'articles': articles})


class ShopView(View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.filter(published=True).all()
        sort = request.GET.getlist('sort')
        products = Gloves.objects.filter(published=True).all().order_by(*sort)
        manufacturer = Manufacturer.objects.all()
        cart_product_form = CartAddProductForm()
        paginator = Paginator(products, 9)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        return render(
            request, 'shop.html', {
                'categories': categories,
                'manufacturer': manufacturer,
                'cart_product_form': cart_product_form,
                'page': page})


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
        context['comments'] = gloves.comments.all()
        return context


class ProductCommentCreateView(CreateView):
    model = Comment
    template_name = 'includes/product_comment_new.html'
    fields = ['author', 'text']


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
        sort = self.request.GET.getlist('sort')
        products = category.category_products.filter(
            published=True).all().order_by(*sort)
        paginator = Paginator(products, 9)
        page_number = self.request.GET.get('page')
        context['page'] = paginator.get_page(page_number)
        context['manufacturer'] = Manufacturer.objects.all()
        context['cart_product_form'] = CartAddProductForm()
        return context


class ManufactureDetailView(CategoryDetailMixin, DetailView):
    model = Manufacturer
    queryset = Manufacturer.objects.all()
    context_object_name = 'manufacture'
    template_name = 'manufacturer.html'
    slug_url_kwarg = 'manufacture_slug'

    def get_context_data(self, **kwargs):
        context = super(ManufactureDetailView, self).get_context_data(**kwargs)
        manufacture = get_object_or_404(
            Manufacturer, slug=self.kwargs.get('manufacture_slug')
            )
        sort = self.request.GET.getlist('sort')
        products = manufacture.manufacturer_products.filter(
            published=True).all().order_by(*sort)
        paginator = Paginator(products, 9)
        page_number = self.request.GET.get('page')
        context['page'] = paginator.get_page(page_number)
        context['manufacturer'] = Manufacturer.objects.all()
        context['cart_product_form'] = CartAddProductForm()
        return context


def page_not_found(request, exception):
    return render(
        request,
        'misc/404.html',
        {'path': request.path},
        status=404
    )


def server_error(request):
    return render(request, 'misc/500.html', status=500)
