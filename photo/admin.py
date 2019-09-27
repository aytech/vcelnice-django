from django.contrib import admin
from .models import Photo


class PhotoAdmin(admin.ModelAdmin):
    fields = ('caption', 'image')
    list_display = ['caption', 'created']

    class Meta:
        model = Photo


admin.site.register(Photo, PhotoAdmin)
