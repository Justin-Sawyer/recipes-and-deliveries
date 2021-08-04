from django import forms
from .models import Recipe, Ingredient
from blog.widgets import CustomClearableFileInput


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        exclude = ('recipe', )

        labels = {
            'quantity': 'Qty',
        }

        placeholders = {
            'preparation': 'eg. Chooped',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            'unit': 'eg: ml',
            'preparation': 'eg: chopped',
            'name': 'eg: tomatoes'
        }

        for field in self.fields:
            if field != 'quantity':
                placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-green'

        self.fields['quantity'].widget.attrs['min'] = 0
        # self.fields['quantity'].widget.attrs['class'] = 'inline border-green col-6 col-md-2'
        # self.fields['unit'].widget.attrs['class'] ='inline border-green col-4 col-md-2'

IngredientFormSet = forms.inlineformset_factory(Recipe, Ingredient,
                                                form=IngredientForm)


class RecipeForm(forms.ModelForm):

    # Replace image field
    image = forms.ImageField(label='Image',
                             required=False,
                             widget=CustomClearableFileInput)


    class Meta:
        model = Recipe
        exclude = ('author', 'date', 'date_posted', 'date_edited')

        labels = {
            'intro': 'Brief Description',
        }
    
    def clean_servings(self):
        value = self.cleaned_data.get('servings')
        print(value)
        if value < 1:
            raise forms.ValidationError('The number of servings must be \
                greater than zero')
        return value
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            'title': 'eg: Carrot Cake',
            'intro': 'eg: A deliciously sweet dessert',
            'prep_time': 'eg: 1hr 20mins',
            'cook_time': 'eg: 1hr 20mins',
            'total_time': 'eg: 1hr 20mins',
            'directions': 'Describe the steps to make this recipe',
            'image': '',
            'image_credit': 'Who took the photo?',
        }

        for field in self.fields:
            if field != 'servings':
                placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-green'

        self.fields['title'].widget.attrs['autofocus'] = True
