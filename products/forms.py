from django import forms
from .widgets import CustomClearableFileInput
from .models import Product, Category


class ProductForm(forms.ModelForm):

    # Replace image field
    image = forms.ImageField(label='Image',
                             required=False,
                             widget=CustomClearableFileInput)

    class Meta():
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_name = [(c.id, c.get_friendly_name()) for c in categories]
        sku = Product.objects.order_by('sku').last()

        placeholders = {
            'sku': f'Greater than {sku.sku}',
        }

        for field in self.fields:
            if field == 'sku':
                placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder

        self.fields['category'].choices = friendly_name
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-primary'
