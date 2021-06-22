from django.urls import path

from . import views

urlpatterns = [
    path('', views.BaseView.as_view(), name='base'),
    path('products/', views.ShopView.as_view(), name='shop'),
    path('products/<int:id>/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('<slug:category_slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
]
