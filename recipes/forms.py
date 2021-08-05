from django import forms
from .models import Recipe, Ingredient, Category, Tag
from blog.widgets import CustomClearableFileInput


class NewCategoriesForm(forms.ModelForm):

    friendly_name = forms.CharField(label='... or add your own categories',
                                    required=False)

    class Meta():
        model = Category
        fields = ('friendly_name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-green'


class NewTagsForm(forms.ModelForm):

    tagname = forms.CharField(label='... or add your own tag', required=False)

    class Meta():
        model = Tag
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-green'


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
            'quantity': 'eg: 0.1',
            'unit': 'eg: ml',
            'preparation': 'eg: chopped',
            'name': 'eg: tomatoes'
        }

        for field in self.fields:
            # if field != 'quantity':
            placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-green'

        self.fields['quantity'].widget.attrs['min'] = 0.01


IngredientFormSet = forms.inlineformset_factory(Recipe, Ingredient,
                                                form=IngredientForm, extra=15)


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
        categories = Category.objects.all().order_by('friendly_name')
        friendly_name = [(c.id, c.get_friendly_name()) for c in categories]

        placeholders = {
            'title': 'eg: Carrot Cake',
            'intro': 'eg: A deliciously sweet dessert',
            'prep_time': 'eg: 1hr 20mins',
            'cook_time': 'eg: 1hr 20mins',
            'total_time': 'eg: 1hr 20mins',
            'directions': 'Describe the steps to make this recipe',
            'image': '',
            'image_credit': 'Who took the photo?',
            'servings': 'No. of servings',
            'tag': '',
            'category': '',
        }

        for field in self.fields:
            placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-green'
        self.fields['category'].choices = friendly_name
        self.fields['title'].widget.attrs['autofocus'] = True
