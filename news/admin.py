from django.contrib import admin
from .forms import ArticleForm
from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    change_form_template = 'admin/change_news_form.html'
    list_display = ['title', 'created', 'updated']
    form = ArticleForm


admin.site.register(Article, ArticleAdmin)
