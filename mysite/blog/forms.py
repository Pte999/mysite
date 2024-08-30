from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = 'title', 'slug', 'author', 'body', 'status'

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('Длина превышает 50 симвлов')
        return title

# class NameForm(forms.Form):
#     def validate_age(value):
#         if value < 0:
#             raise ValidationError(
#                 ('%(value)s неверно введенный возраст!'),
#                 params={'value':value}
#             )
#
#     name = forms.CharField(label='Имя', disabled=True, initial='Evgeny')
#     last_name = forms.CharField(label='Фамилия', required=False)
#     age = forms.IntegerField(label='Возраст', validators=[validate_age, MinValueValidator(10)])
#     about = forms.CharField(widget=forms.Textarea)