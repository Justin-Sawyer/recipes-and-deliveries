from django import forms
from .widgets import CustomClearableFileInput
# from django.contrib.auth.models import User
from .models import Post, Category, Tag, Comment


class NewCategoriesForm(forms.ModelForm):

    friendly_name = forms.CharField(label='... or add your own category',
                                    required=False)

    class Meta():
        model = Category
        fields = ('friendly_name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            'friendly_name': 'One single word only'
        }

        for field in self.fields:
            placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder


class NewTagsForm(forms.ModelForm):

    tagname = forms.CharField(label='... or add your own tag', required=False)

    class Meta():
        model = Tag
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            'tagname': 'One single word only'
        }

        for field in self.fields:
            placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder


class BlogPostForm(forms.ModelForm):

    # Replace image field
    image = forms.ImageField(label='Image',
                             required=False,
                             widget=CustomClearableFileInput)

    # Change rendering of form to user-friendly checkboxes
    # Credit:
    # https://medium.com/swlh/django-forms-for-many-to-many-fields-d977dec4b024
    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        label='Choose some categories from the list',
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    # Change rendering of form to user-friendly checkboxes
    # Credit:
    # https://medium.com/swlh/django-forms-for-many-to-many-fields-d977dec4b024
    tag =  forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        label='Choose some tags from the list',
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

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

        placeholders = {
            'title': 'Add Your Title',
            'tagline': 'Describe your article',
            'image_credit': 'Who took the photo?',
            'content': 'Add your content here.',
            'category': '',
            'tag': '',
            'image': '',
        }

        self.fields['title'].widget.attrs['autofocus'] = True

        for field in self.fields:
            placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder

        self.fields['category'].choices = friendly_name

class CommentForm(forms.ModelForm):

    class Meta():
        labels = {
            # 'name': 'Name*',
            'body': 'Add your comment',
        }

        model = Comment
        fields = ('body', )
