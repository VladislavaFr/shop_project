from django import forms
from .models import Product
from django.core.exceptions import ValidationError

# Запрещенные слова для имени и описания
FORBIDDEN_WORDS = [
    'казино', 'криптовалюта', 'крипта', 'биржа',
    'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
]

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'available', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Стилизация полей
        for field_name, field in self.fields.items():
            if isinstance(field, forms.BooleanField):
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                field.widget.attrs.update({'class': 'form-control'})

    # Валидация имени
    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        for word in FORBIDDEN_WORDS:
            if word.lower() in name.lower():
                raise ValidationError(f"Имя продукта не может содержать слово '{word}'")
        return name

    # Валидация описания
    def clean_description(self):
        description = self.cleaned_data.get('description', '')
        for word in FORBIDDEN_WORDS:
            if word.lower() in description.lower():
                raise ValidationError(f"Описание продукта не может содержать слово '{word}'")
        return description

    # Валидация цены
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise ValidationError("Цена продукта не может быть отрицательной")
        return price

    # Валидация изображения
    def clean_image(self):
        image = self.cleaned_data.get('image')

        # Если изображения нет или это уже существующее изображение
        if not image or hasattr(image, 'url'):
            return image

        if image:
            if image.size > 5 * 1024 * 1024:
                raise ValidationError("Размер изображения не должен превышать 5 МБ.")

            content_type = getattr(image, 'content_type', None)
            if content_type and content_type not in ['image/jpeg', 'image/png']:
                raise ValidationError("Разрешены только форматы JPEG и PNG.")

        return image
