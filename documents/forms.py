from django import forms
from .models import Document
import os


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['description', 'file']

    def clean_file(self):
        doc = self.cleaned_data.get('file')
        allowed_extensions = ('.pdf', '.doc')
        name, extension = os.path.splitext(doc.name)

        if extension not in allowed_extensions:
            raise forms.ValidationError('Invalid file, please upload only .PDF or .DOC files')

        return doc
