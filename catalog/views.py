from django.shortcuts import render
from .models import Product


def product_list(request):
    """Главная страница: список всех товаров"""
    products = Product.objects.all()
    return render(request, 'catalog/product_list.html', {'products': products})