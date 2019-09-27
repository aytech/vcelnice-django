from django.shortcuts import render
from .models import Video
from vcelnice.settings import *
import os


def home(request):
    videos = Video.objects.filter(youtube_status__gt=YOUTUBE_STATUS_PENDING_UPLOAD)

    for video in videos:
        thumb_path = os.path.join(MEDIA_ROOT, video.thumb.name)
        if not os.path.exists(thumb_path):
            video.thumb = FALLBACK_IMAGES_NATURE_URL
        else:
            video.thumb = os.path.join(MEDIA_URL, video.thumb.name)

    context = {
        'gallery': videos
    }
    return render(request, 'video.html', context)
