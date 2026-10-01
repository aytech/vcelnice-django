from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget

from .models import Article


class ArticleForm(forms.ModelForm):
    text = forms.CharField(
        widget=CKEditor5Widget(
            attrs={"class": "django_ckeditor_5"},
            config_name="extends",
        )
    )

    class Meta:
        model = Article
        fields = ['title', 'text', 'icon']
