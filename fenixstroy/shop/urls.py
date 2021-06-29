from django.urls import path

from . import views

urlpatterns = [
    path('', views.BaseView.as_view(), name='base'),
    path('shop/products/', views.ShopView.as_view(), name='shop'),
    path(
        'shop/products/<int:id>/<slug:slug>/',
        views.ProductDetailView.as_view(),
        name='product_detail'),
    path(
        'shop/category/<slug:category_slug>/',
        views.CategoryDetailView.as_view(),
        name='category_detail'),
    path(
        'shop/manufacture/<slug:manufacture_slug>/',
        views.ManufactureDetailView.as_view(),
        name='manufacture_detail'),
]
