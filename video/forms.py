from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Video
import os


class VideoForm(forms.ModelForm):
    ALLOWED_VIDEO_EXTENSIONS = ['.mp4', '.avi', '.wmv', '.mov', '.mpeg4', '.mpegps', '.flv', '.3gpp', '.webm']

    class Meta:
        model = Video
        fields = ['caption', 'description', 'youtube_id', 'thumb', 'file']

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if not file:
            return file
        extension = os.path.splitext(file.name)[1].lower()
        if extension not in self.ALLOWED_VIDEO_EXTENSIONS:
            raise forms.ValidationError(_('Invalid file, allowed files must have one of these extensions: ') +
                                        ', '.join(self.ALLOWED_VIDEO_EXTENSIONS))
        return file
