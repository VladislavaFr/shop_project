from django import forms
from django.core.exceptions import ValidationError
from .models import Product

FORBIDDEN_WORDS = [
    "казино", "криптовалюта", "крипта", "биржа",
    "дешево", "бесплатно", "обман", "полиция", "радар"
]

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'available', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['available'].widget.attrs.update({'class': 'form-check-input'})

    def clean_name(self):
        name = self.cleaned_data.get('name', '').lower()
        for word in FORBIDDEN_WORDS:
            if word in name:
                raise ValidationError(f"Название продукта не должно содержать запрещенные слова: {word}")
        return self.cleaned_data['name']

    def clean_description(self):
        description = self.cleaned_data.get('description', '').lower()
        for word in FORBIDDEN_WORDS:
            if word in description:
                raise ValidationError(f"Описание продукта не должно содержать запрещенные слова: {word}")
        return self.cleaned_data['description']

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise ValidationError("Цена не может быть отрицательной.")
        return price

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 5 * 1024 * 1024:
                raise ValidationError("Размер изображения не должен превышать 5 МБ.")
            if not image.content_type in ['image/jpeg', 'image/png']:
                raise ValidationError("Разрешены только форматы JPEG и PNG.")
        return image
