from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('', views.main, name='main'),
    path(
        'category/<int:category_id>', 
        views.category_products,
        name='category_products'
    ),
    path(
        '<slug:slug>/',
        views.ProductDetailView.as_view(),
        name='product-detail'
    ),
]
