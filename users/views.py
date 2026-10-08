from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from catalog.models import Product


def register(request):
    """Регистрация нового пользователя"""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    """Страница профиля пользователя"""
    products = Product.objects.filter(author=request.user)
    return render(request, 'users/profile.html', {
        'products': products,
    })
