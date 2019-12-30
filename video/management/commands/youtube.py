import json
import logging
import os

import httplib2
from django.core.management import BaseCommand
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from vcelnice.settings import MEDIA_ROOT
from video.models import Video


class Youtube(BaseCommand):
    CLIENT_SECRET_FILE = "client_secret.json"
    MAX_RETRIES = 10
    OAUTH_FILE = "youtube-oauth2.json"
    RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError)
    RETRIABLE_STATUS_CODES = [500, 502, 503, 504]
    SCOPES = ["https://www.googleapis.com/auth/youtube"]
    SERVICE_NAME = "youtube"
    API_VERSION = "v3"

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger("vcelnice.info")
        self.youtube = self.get_youtube_service()

    def handle(self, *args, **options):
        pass

    def get_youtube_service(self):
        credentials_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.OAUTH_FILE)
        with open(credentials_file, "r") as token_file:
            token = json.load(token_file)
            credentials = Credentials(**token)
        return build(self.SERVICE_NAME, self.API_VERSION, credentials=credentials)

    def upload_thumbnail(self, video_id, filename):
        if filename == '':
            return

        file_path = os.path.join(MEDIA_ROOT, filename)

        if not os.path.exists(file_path):
            return self.logger.error('Thumbnail %s for youtube video %i not found' % (filename, video_id))

        try:
            self.youtube.thumbnails().set(
                videoId=video_id,
                media_body=os.path.join(MEDIA_ROOT, filename)
            ).execute()
            self.logger.info("Thumbnail %s updated for video %s" % (filename, video_id))
        except HttpError as e:
            self.logger.critical(
                "An HTTP error %d occurred while uploading video thumbnail: %s" % (e.resp.status, e.content))

    @staticmethod
    def get_videos(status):
        # noinspection PyUnresolvedReferences
        return Video.objects.filter(youtube_status__in=[status])
