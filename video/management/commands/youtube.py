from django.core.management.base import BaseCommand
from vcelnice.common.youtube import Youtube
from video.models import Video
from vcelnice.settings import *
import logging


class Command(BaseCommand):
    """ Upload videos to youtube """

    def __init__(self):
        self.logger = logging.getLogger('vcelnice.info')

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        video_set = Video.objects.filter(
            youtube_status__in=[YOUTUBE_STATUS_PENDING_UPLOAD, YOUTUBE_STATUS_PENDING_UPDATE,
                                YOUTUBE_STATUS_PENDING_DELETE])

        if video_set is None:
            exit()

        video = video_set[0]
        youtube = Youtube()

        if video.youtube_status == YOUTUBE_STATUS_PENDING_UPLOAD:
            return youtube.upload(video)

        if video.youtube_status == YOUTUBE_STATUS_PENDING_UPDATE:
            if youtube.update_video(video):
                video.save_upload_status()
            return

        if video.youtube_status == YOUTUBE_STATUS_PENDING_DELETE:
            if youtube.delete_video(video.youtube_id):
                video.save_deleted_status()
                video.delete()
