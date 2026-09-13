import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.test import TransactionTestCase, override_settings


class RemoveVideoFileMigrationTests(TransactionTestCase):
    migrate_from = [('video', '0004_remove_youtube_upload_workflow')]
    migrate_to = [('video', '0005_remove_video_file')]

    def test_file_column_is_removed_without_deleting_videos_thumbnails_or_stored_files(self):
        # Use only the test database and a temporary media directory.
        with tempfile.TemporaryDirectory() as media_root, override_settings(MEDIA_ROOT=media_root):
            executor = MigrationExecutor(connection)
            final_targets = executor.loader.graph.leaf_nodes()
            try:
                executor.migrate(self.migrate_from)
                old_apps = executor.loader.project_state(self.migrate_from).apps
                old_video = old_apps.get_model('video', 'Video')
                record = old_video.objects.create(
                    caption='Existing video', description='Keep this description',
                    youtube_id='qH6i5JsntCw', thumb='video/thumbnail.jpg',
                    file=SimpleUploadedFile('original.mp4', b'original-video-bytes'),
                )
                old_video.objects.create(caption='Draft without a file', youtube_id=None)
                storage, original_name = record.file.storage, record.file.name
                retained_fields = ('id', 'caption', 'description', 'youtube_id', 'thumb', 'created', 'updated')
                before = list(old_video.objects.order_by('id').values(*retained_fields))

                executor = MigrationExecutor(connection)
                executor.migrate(self.migrate_to)
                new_apps = executor.loader.project_state(self.migrate_to).apps
                video = new_apps.get_model('video', 'Video')

                self.assertEqual(before, list(video.objects.order_by('id').values(*retained_fields)))
                with connection.cursor() as cursor:
                    columns = {column.name for column in connection.introspection.get_table_description(cursor, 'video_video')}
                self.assertNotIn('file', columns)
                self.assertIn('thumb', columns)
                self.assertTrue(storage.exists(original_name))
                with storage.open(original_name, 'rb') as original:
                    self.assertEqual(original.read(), b'original-video-bytes')
            finally:
                MigrationExecutor(connection).migrate(final_targets)
