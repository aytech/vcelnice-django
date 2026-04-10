import os

from django.conf import settings
from django.shortcuts import render

from .models import Video


def home(request):
    videos = Video.objects.filter(youtube_status__gt=settings.YOUTUBE_STATUS_PENDING_UPLOAD)

    for video in videos:
        thumb_path = os.path.join(settings.MEDIA_ROOT, video.thumb.name)
        if not os.path.exists(thumb_path):
            video.thumb = settings.FALLBACK_IMAGES_NATURE_URL
        else:
            video.thumb = os.path.join(settings.MEDIA_URL, video.thumb.name)

    context = {
        'gallery': videos
    }
    return render(request, 'video.html', context)
