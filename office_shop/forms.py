from django import forms
from office_shop.models import Product


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('category', 'name', 'retail_price', 'description', 'image')
