from googleapiclient.errors import HttpError

from vcelnice.settings import YOUTUBE_STATUS_PENDING_UPDATE, YOUTUBE_STATUS_UPLOADED
from video.management.commands.youtube import Youtube


class Command(Youtube):
    def __init__(self):
        super().__init__()

    def handle(self, *args, **options):
        query_set = self.get_videos(status=YOUTUBE_STATUS_PENDING_UPDATE)
        if query_set.count() > 0:
            self.update(query_set.first())

    def update(self, video):
        if video.tags is not None:
            tags = [tag.strip() for tag in video.tags.split(',')]
        else:
            tags = None
        try:
            self.youtube.videos().update(
                part='snippet',
                body=dict(
                    snippet=dict(
                        title=video.caption,
                        description=video.description,
                        tags=tags,
                        categoryId=int(video.category)
                    ),
                    id=video.youtube_id
                )
            ).execute()
            self.upload_thumbnail(video.youtube_id, video.thumb.name)
            video.save_upload_status(YOUTUBE_STATUS_UPLOADED)
            self.logger.info("Video id '%s' was successfully updated." % video.youtube_id)
        except HttpError as e:
            self.logger.critical(
                "An HTTP error %d occurred while updating video %s: %s" % (video.youtube_id, e.resp.status, e.content))
