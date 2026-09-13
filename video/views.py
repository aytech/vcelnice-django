import os

from django.conf import settings
from django.shortcuts import render

from .models import Video


def home(request):
    videos = Video.objects.exclude(youtube_id__isnull=True).exclude(youtube_id="")

    for video in videos:
        thumb_path = os.path.join(settings.MEDIA_ROOT, video.thumb.name) if video.thumb else None
        if not thumb_path or not os.path.isfile(thumb_path):
            video.thumb = settings.FALLBACK_IMAGES_NATURE_URL
        else:
            video.thumb = os.path.join(settings.MEDIA_URL, video.thumb.name)

    context = {
        'gallery': videos
    }
    return render(request, 'video.html', context)
