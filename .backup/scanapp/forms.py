from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_id', 'name', 'customer_price', 'retail_price', 'notes']
        widgets = {
            'product_id': forms.TextInput(attrs={'readonly': 'readonly'}),  # Make product_id read-only
        }
