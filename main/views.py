from django.shortcuts import render
from django.views.generic.detail import DetailView

from .models import Category, Product


def main(request):
    categories = Category.objects.filter(is_active=True)
    context = {
        'categories': categories
    }
    return render(request, 'main/main.html', context)


def category_products(request, category_id: int):
    '''
    страница товаров для категории
    '''
    products = Product.objects.filter(category_id=category_id)
    context = {
        'products': products
    }
    return render(request, 'main/product/list.html', context)

class ProductDetailView(DetailView):
    model=Product
    template_name='main/product/detail.html'
    context_object_name='product'