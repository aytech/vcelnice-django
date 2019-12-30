from googleapiclient.errors import HttpError

from vcelnice.settings import YOUTUBE_STATUS_PENDING_DELETE, YOUTUBE_STATUS_DELETED
from video.management.commands.youtube import Youtube


class Command(Youtube):
    def __init__(self):
        super().__init__()

    def handle(self, *args, **options):
        query_set = self.get_videos(status=YOUTUBE_STATUS_PENDING_DELETE)
        if query_set.count() > 0:
            self.delete(query_set.first())

    def delete(self, video):
        try:
            self.youtube.videos().delete(id=video.youtube_id).execute()
            video.save_upload_status(YOUTUBE_STATUS_DELETED)
            video.delete()
            self.logger.info('Youtube video %s was successfully deleted' % video.youtube_id)
        except HttpError as e:
            self.logger.critical(
                "An HTTP error %d occurred while deleting video: %s" % (e.resp.status, e.content))
