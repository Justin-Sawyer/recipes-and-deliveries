from django import forms
from .widgets import CustomClearableFileInput
from django.contrib.auth.models import User
from .models import Post, Category, Tag


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


class BlogPostForm(forms.ModelForm):

    # Replace image field
    image = forms.ImageField(label='Image',
                             required=False,
                             widget=CustomClearableFileInput)

    class Meta():
        model = Post
        exclude = ('author', 'date_posted',)
        labels = {
            'tagline': 'Description',
            'category': 'Choose some categories from the list',
            'tag': 'Choose some tags from the list',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all().order_by('friendly_name')
        friendly_name = [(c.id, c.get_friendly_name()) for c in categories]
        # categories = forms.MultipleChoiceField(widget=forms.SelectMultiple,
                                             # choices=friendly_name)

        placeholders = {
            'title': 'Add Your Title',
            'tagline': 'Describe your article',
            'image_credit': 'Who took the photo?',
            'content': 'Add your content here.'
        }

        self.fields['title'].widget.attrs['autofocus'] = True

        for field in self.fields:
            if field == 'title':
                placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            if field == 'tagline':
                placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            if field == 'image_credit':
                placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            if field == 'content':
                placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder

        self.fields['category'].choices = friendly_name
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-green'
