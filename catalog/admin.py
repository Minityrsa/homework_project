from django.contrib import admin
from .models import Product, Category, Manufacturer


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'website')
    search_fields = ('name', 'country')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'seller', 'category', 'manufacturer', 'status', 'created_at')
    list_filter = ('status', 'category', 'manufacturer')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at',)
