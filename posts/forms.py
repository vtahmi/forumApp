from crispy_forms.helper import FormHelper
from django import forms
from django.core.exceptions import ValidationError
from django.forms import formset_factory

from posts.mixins import ReadOnlyMixin
from posts.models import Post, Comment
from posts.validators import BadWordValidator


# class MyForm(forms.Form):
#     CHOICES = [
#         ('option1', 'Option 1'),
#         ('option2', 'Option 2'),
#         ('option3', 'Option 3'),
#     ]
#     first_name = forms.CharField(max_length=30, label='First Name')
#     last_name = forms.CharField(max_length=30, label='Last Name')
#     password = forms.CharField(max_length=10, label='My password', widget=forms.PasswordInput)
#     email = forms.EmailField(label='Email Address')
#     my_text = forms.CharField(widget=forms.Textarea())
#     my_number = forms.IntegerField()
#     radio = forms.ChoiceField(
#         choices=CHOICES,
#         widget=forms.RadioSelect
#     )
#     multiple_choices = forms.MultipleChoiceField(
#         choices=CHOICES,
#         widget=forms.CheckboxSelectMultiple
#     )


class PostForm(forms.ModelForm):
    # content2 = (forms.CharField(
    #     min_length=3,
    #     validators=[BadWordValidator(bad_words=['bad', 'ugly', 'stupid'])],
    #     error_messages={
    #         'min_length': 'Content2 must be at least 3 characters long.'}
    # ))

    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'language': forms.RadioSelect(attrs={'class': 'language-select'}),
            'date_created': forms.DateTimeInput(format='%d/%m/%Y %H:%M'),
        }
        error_messages={
            'author': {
                'max_length': "That's too long for a name!"
            }
        }

    def clean_author(self):
        author = self.cleaned_data.get('author')
        if not author.isalpha():
            raise ValidationError('Author name must contain only alphabetic characters.')
        return author
    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')

        if title in content:
            raise ValidationError(
                "The content should not contain the title."
            )


        return cleaned_data
    def save(self, commit=True):
        post = super().save(commit=False)
        post.author = post.author.capitalize()
        if commit:
            post.save()
        return post
class PostCreateForm(PostForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'

class PostEditForm(PostForm):
    pass

class PostDeleteForm(ReadOnlyMixin, PostForm):
    pass


class PostSearchForm(forms.Form):
    query = forms.CharField(
        max_length=100, required=False,
        label='', widget=forms.TextInput(attrs={'placeholder': 'Enter search term...'}
    ))


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': ''
        }
        widgets = {
            'content': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter your comment here...'
                }
            )
        }
CommentFormSet = formset_factory(
    CommentForm,
    extra=1,
    can_delete=True
)
































