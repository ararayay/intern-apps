from django import forms


# Форма для генерации QR-кода для товара
class GenerateQR(forms.Form):
    name = forms.CharField(
        label="Название товара",
        widget=forms.TextInput(attrs={
            'id': 'product-autocomplete',
            'autocomplete': 'off',
            'placeholder': 'Введите название товара'
        })
    )
    product_id = forms.CharField(widget=forms.HiddenInput(), required=False)