from django.contrib import admin
from home.forms import HomeForm
from home.models import Home


class HomeAdmin(admin.ModelAdmin):
    change_form_template = 'admin/change_home_form.html'
    list_display = ['title', 'icon']
    form = HomeForm


admin.site.register(Home, HomeAdmin)
