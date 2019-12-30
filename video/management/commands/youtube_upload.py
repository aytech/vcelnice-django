import random
import time

from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

from video.management.commands.youtube import Youtube
from vcelnice.settings import *


class Command(Youtube):
    """ Upload videos to youtube """

    def __init__(self):
        super().__init__()

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        query_set = self.get_videos(status=YOUTUBE_STATUS_PENDING_UPLOAD)
        if query_set.count() > 0:
            self.upload(query_set.first())

        # if video.youtube_status == YOUTUBE_STATUS_PENDING_UPDATE:
        #     if youtube.update_video(video):
        #         video.save_upload_status()
        #     return

        # if video.youtube_status == YOUTUBE_STATUS_PENDING_DELETE:
        #     if youtube.delete_video(video.youtube_id):
        #         video.save_deleted_status()
        #         video.delete()

    def upload(self, video):
        if video.tags is not None:
            tags = [tag.strip() for tag in video.tags.split(',')]
        else:
            tags = None
        file_path = os.path.join(MEDIA_ROOT, video.file.name)
        body = dict(
            snippet=dict(
                title=video.caption,
                description=video.description,
                tags=tags
            ),
            status=dict(
                privacyStatus="public"
            )
        )
        insert_request = self.youtube.videos().insert(
            part=",".join(body.keys()),
            body=body,
            # The chunksize parameter specifies the size of each chunk of data, in
            # bytes, that will be uploaded at a time. Set a higher value for
            # reliable connections as fewer chunks lead to faster uploads. Set a lower
            # value for better recovery on less reliable connections.
            #
            # Setting "chunksize" equal to -1 in the code below means that the entire
            # file will be uploaded in a single HTTP request. (If the upload fails,
            # it will still be retried where it left off.) This is usually a best
            # practice, but if you're using Python older than 2.6 or if you're
            # running on App Engine, you should set the chunksize to something like
            # 1024 * 1024 (1 megabyte).
            media_body=MediaFileUpload(file_path, chunksize=-1, resumable=True)
        )
        self.resumable_upload(insert_request, video)

    def resumable_upload(self, request, video):
        response = None
        error = None
        retry = 0

        while response is None:
            try:
                status, response = request.next_chunk()
                if response is not None:
                    if 'id' in response:
                        video.youtube_id = response['id']
                        video.save()
                        video.save_upload_status(YOUTUBE_STATUS_UPLOADED)
                        self.upload_thumbnail(response['id'], video.thumb.name)
                        self.logger.info("Video id '%s' was successfully uploaded." % response['id'])
                    else:
                        self.logger.error('The upload failed with an unexpected response: %s' % response)
                        exit()
            except HttpError as e:
                if e.resp.status in self.RETRIABLE_STATUS_CODES:
                    error = 'A retriable HTTP error %d occurred:\n%s' % (e.resp.status, e.content)
                else:
                    raise
            except self.RETRIABLE_EXCEPTIONS as e:
                error = 'A retriable error occurred: %s' % e

            if error is not None:
                self.logger.error(error)
                retry += 1
                if retry > self.MAX_RETRIES:
                    self.logger.error('Youtube upload interrupted, reason: number of attempts exceeded')
                    exit()

                max_sleep = 2 ** retry
                sleep_seconds = random.random() * max_sleep
                self.logger.info("Sleeping %f seconds and then retrying..." % sleep_seconds)
                time.sleep(sleep_seconds)
