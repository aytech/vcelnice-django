from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Video
import os


class VideoForm(forms.ModelForm):
    # https://support.google.com/youtube/troubleshooter/2888402
    ALLOWED_VIDEO_EXTENSIONS = ['.mp4', '.avi', '.wmv', '.mov', '.mpeg4', '.mpegps', '.flv', '.3gpp', '.webm']

    class Meta:
        model = Video
        fields = ['caption', 'description', 'file', 'thumb', 'category', 'tags']

    def clean_file(self):
        file = self.cleaned_data.get('file')
        filename, extension = os.path.splitext(file.name)
        if extension not in self.ALLOWED_VIDEO_EXTENSIONS:
            raise forms.ValidationError(_('Invalid file, allowed files must have one of these extensions: ') +
                                        ', '.join(self.ALLOWED_VIDEO_EXTENSIONS))
        return file
