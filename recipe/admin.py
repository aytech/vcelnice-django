from django.contrib import admin
from .forms import RecipeForm
from .models import Recipe


class RecipeAdmin(admin.ModelAdmin):
    change_form_template = 'admin/change_recipe_form.html'
    list_display = ['title', 'created', 'updated']
    form = RecipeForm

admin.site.register(Recipe, RecipeAdmin)
