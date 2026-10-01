from django.contrib import admin
from .forms import RecipeForm
from .models import Recipe


class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title', 'created', 'updated']
    form = RecipeForm

admin.site.register(Recipe, RecipeAdmin)
