from django import forms
from .models import Tank, Quotation

class QuotationForm(forms.ModelForm):
    class Meta:
        model = Quotation
        fields = '__all__'

class ProductForm(forms.ModelForm):
    class Meta:
        model = Tank
        fields = '__all__'
        exclude = ['quotation', 'volume']