from video.management.commands.youtube import Youtube
from video.models import VideoCategory


class Command(Youtube):
    def __init__(self):
        super().__init__()

    def handle(self, *args, **options):
        categories = self.youtube.videoCategories().list(part="snippet", regionCode="CZ").execute()
        for category in categories["items"]:
            if category["snippet"]["assignable"]:
                model = VideoCategory()
                model.category_id = category["id"]
                model.title = category["snippet"]["title"]
                model.save()
