from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product
from .forms import ProductForm


def product_list(request):
    """Главная страница: список всех товаров"""
    products = Product.objects.all()
    return render(request, 'catalog/product_list.html', {'products': products})


@login_required
def product_add(request):
    """Страница добавления нового товара"""
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.author = request.user
            product.save()
            return redirect('product_list')
    else:
        form = ProductForm()

    return render(request, 'catalog/product_form.html', {
        'form': form,
        'title': 'Добавить товар',
        'button_text': 'Сохранить товар',
    })


@login_required
def product_edit(request, pk):
    """Страница редактирования товара"""
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)

    return render(request, 'catalog/product_form.html', {
        'form': form,
        'title': 'Редактировать товар',
        'button_text': 'Сохранить изменения',
    })


@login_required
def product_delete(request, pk):
    """Страница удаления товара с подтверждением"""
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.delete()
        return redirect('product_list')

    return render(request, 'catalog/product_confirm_delete.html', {'product': product})
