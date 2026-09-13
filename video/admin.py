from django.contrib import admin

from .forms import VideoForm
from .models import Video


class VideoAdmin(admin.ModelAdmin):
    form = VideoForm
    list_display = ['caption', 'created', 'youtube_id']
    fields = ('caption', 'description', 'youtube_id', 'thumb')


admin.site.register(Video, VideoAdmin)
