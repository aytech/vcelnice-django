from django.contrib import admin
from home.forms import HomeForm
from home.models import Home


class HomeAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon']
    form = HomeForm


admin.site.register(Home, HomeAdmin)
