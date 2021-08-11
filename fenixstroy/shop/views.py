from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.db.models import Avg
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DeleteView, DetailView, ListView, TemplateView
from django.views.generic.base import View
from django.views.generic.edit import CreateView

from blog.models import Article
from cart.forms import CartAddProductForm

from .forms import CommentForm, RatingForm
from .mixins import CategoryDetailMixin
from .models import Category, Comment, Gloves, LatestProducts, Manufacturer

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
        glove = get_object_or_404(
            Gloves, pk=self.kwargs.get('id'), slug=self.kwargs.get('slug')
            )
        context['comments'] = glove.comments.all()
        # if context['comments']:
        #     price_score = context['comments'].aggregate(
        #         Avg('price_score')
        #         )['price_score__avg']
        #     quality_score = context['comments'].aggregate(
        #         Avg('quality_score')
        #         )['quality_score__avg']
        #     context['int_rating'] = (price_score + quality_score) / 2
        context['cart_product_form'] = CartAddProductForm()
        context['star_form'] = RatingForm()
        context['form'] = CommentForm()
        return context


class ProductCommentCreateView(TemplateView):
    rating_form = RatingForm
    comment_form = CommentForm
    template_name = 'product_detail.html'

    def post(self, request, id, slug):
        product = get_object_or_404(
            Gloves, id=id, slug=slug
            )
        post_data = request.POST or None
        rating_form = RatingForm(post_data)
        comment_form = CommentForm(post_data)

        if rating_form.is_valid() and comment_form.is_valid():
            rating = rating_form.save(commit=False)
            rating.product = product
            rating.save()
            comment = comment_form.save(commit=False)
            comment.product = product
            comment.save()
            return redirect('product_detail', id=product.id, slug=product.slug)

        context = self.get_context_data(
            rating_form=rating_form,
            comment_form=comment_form,
            product=product
            )
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


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
