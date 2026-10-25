from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from .models import Product, Category, Tag
from .forms import ProductForm


class ProductListView(ListView):
    """Список всех товаров + фильтр по категориям"""
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        qs = super().get_queryset()
        category_slug = self.request.GET.get('category')
        if category_slug:
            qs = qs.filter(category__slug=category_slug)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['categories'] = Category.objects.all()
        category_slug = self.request.GET.get('category')
        if category_slug:
            ctx['current_category'] = get_object_or_404(Category, slug=category_slug)
        return ctx


class ProductByTagView(ListView):
    """Товары по конкретному тегу"""
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        return Product.objects.filter(tags=self.tag)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['categories'] = Category.objects.all()
        ctx['current_tag'] = self.tag
        return ctx


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Добавление товара"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('product_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Добавить товар'
        ctx['button_text'] = 'Сохранить товар'
        return ctx

    def form_valid(self, form):
        form.instance.seller = self.request.user
        form.instance.status = Product.Status.PENDING
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование товара"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('product_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Редактировать товар'
        ctx['button_text'] = 'Сохранить изменения'
        return ctx


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление товара с подтверждением"""
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')
    context_object_name = 'product'
