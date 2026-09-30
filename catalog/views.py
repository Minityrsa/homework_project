from django.shortcuts import render, redirect
from .models import Product
from .forms import ProductForm


def product_list(request):
    """Главная страница: список всех товаров"""
    products = Product.objects.all()
    return render(request, 'catalog/product_list.html', {'products': products})


def product_add(request):
    """Страница добавления нового товара"""
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
        # если форма невалидна — просто показываем её с ошибками
    else:
        form = ProductForm()

    return render(request, 'catalog/product_form.html', {'form': form})