from django import forms

from ..models.Product import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'value', 'imagePath')