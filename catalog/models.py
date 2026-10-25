from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Category(models.Model):
    """Категория товаров"""
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")
    slug = models.SlugField(max_length=100, unique=True, blank=True, verbose_name="Слаг")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Manufacturer(models.Model):
    """Производитель товаров"""
    name = models.CharField(max_length=200, verbose_name="Название")
    country = models.CharField(max_length=100, verbose_name="Страна")
    website = models.URLField(blank=True, verbose_name="Сайт")
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Производитель"
        verbose_name_plural = "Производители"
        ordering = ['name']

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Метка (тег) товара"""
    name = models.CharField(max_length=50, unique=True, verbose_name="Название")
    slug = models.SlugField(max_length=50, unique=True, blank=True, verbose_name="Слаг")

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    """Модель товара интернет-магазина"""

    class Status(models.TextChoices):
        PENDING = 'pending', 'На проверке'
        PUBLISHED = 'published', 'Опубликовано'
        REJECTED = 'rejected', 'Отклонено'

    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Изображение")
    seller = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='products',
        verbose_name="Продавец", null=True, blank=True,
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name='products',
        verbose_name="Категория", null=True, blank=True,
    )
    manufacturer = models.ForeignKey(
        Manufacturer, on_delete=models.SET_NULL, related_name='products',
        verbose_name="Производитель", null=True, blank=True,
    )
    tags = models.ManyToManyField(Tag, related_name='products', blank=True, verbose_name="Теги")
    status = models.CharField(
        max_length=20, choices=Status.choices,
        default=Status.PENDING, verbose_name="Статус",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['-created_at']

    def __str__(self):
        return self.name
