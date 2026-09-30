from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    """Форма добавления товара с валидацией"""

    class Meta:
        model = Product
        fields = ['name', 'description', 'price']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Например: Ноутбук',
                'class': 'form-input',
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Краткое описание товара',
                'rows': 3,
                'class': 'form-input',
            }),
            'price': forms.NumberInput(attrs={
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0',
                'class': 'form-input',
            }),
        }
        labels = {
            'name': 'Название товара',
            'description': 'Описание',
            'price': 'Цена (₽)',
        }

    def clean_name(self):
        """Проверка: минимум 6 символов в названии"""
        name = self.cleaned_data.get('name', '').strip()

        if not name:
            raise forms.ValidationError("Название не может быть пустым.")

        if len(name) < 6:
            raise forms.ValidationError(
                f"Название должно содержать минимум 6 символов. "
                f"У вас — {len(name)}."
            )

        return name

    def clean_price(self):
        """Проверка: цена больше 0"""
        price = self.cleaned_data.get('price')

        if price is None:
            raise forms.ValidationError("Укажите цену товара.")

        if price <= 0:
            raise forms.ValidationError("Цена должна быть больше 0.")

        return price
