from django.contrib import admin
from .forms import DocumentForm
from .models import Certificate


class DocumentAdmin(admin.ModelAdmin):
    form = DocumentForm
    list_display = ['description', 'file', 'type']


admin.site.register(Certificate, DocumentAdmin)
