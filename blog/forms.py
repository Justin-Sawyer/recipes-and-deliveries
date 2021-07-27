from django import forms
from .widgets import CustomClearableFileInput
from .models import Post, Category, Tag


class BlogPostForm(forms.ModelForm):

    # Replace image field
    image = forms.ImageField(label='Image',
                             required=False,
                             widget=CustomClearableFileInput)

    class Meta():
        model = Post
        # fields = '__all__'
        exclude = ('date_posted'),

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_name = [(c.id, c.get_friendly_name()) for c in categories]
        tags = Tag.objects.all()
        tagname = [t.tagname.capitalize() for t in tags]
        title = Post.objects.order_by('title').last()

        placeholders = {
            'title': 'Add Your Title',
            'tagline': 'Describe the article in a few short sentences',
            'image_credit': 'Who took the photo?',
            'content': f'Add your content here. \
                \nUsing the "return" key once will move to new lines. \
                \n\nAnd twice will give you a blank line. \
                \n\nHappy blogging!'
        }

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
        # self.fields['tagname'].choices = tagname
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-green'
