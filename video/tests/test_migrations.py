from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.test import TransactionTestCase


class RemoveYouTubeWorkflowMigrationTests(TransactionTestCase):
    migrate_from = [('video', '0003_auto_20200111_2302')]
    migrate_to = [('video', '0004_remove_youtube_upload_workflow')]

    def test_existing_videos_and_media_references_survive_removing_upload_metadata(self):
        # Django's test runner supplies an isolated test database, never the site's database.
        executor = MigrationExecutor(connection)
        final_targets = executor.loader.graph.leaf_nodes()
        try:
            executor.migrate(self.migrate_from)
            old_apps = executor.loader.project_state(self.migrate_from).apps
            old_video = old_apps.get_model('video', 'Video')
            old_apps.get_model('video', 'VideoCategory').objects.create(category_id='1', title='Category')
            records = [
                old_video.objects.create(
                    caption=f'Existing video {status}', description='Original description',
                    youtube_id='qH6i5JsntCw' if status in (2, 3, 4, 5) else None,
                    file=f'youtube/original-{status}.wmv', thumb=f'video/thumb-{status}.jpg',
                    category='1', tags='bees, honey', youtube_status=status,
                )
                for status in (1, 2, 3, 4, 5, None)
            ]
            retained_fields = ('id', 'caption', 'description', 'youtube_id', 'file', 'thumb', 'created', 'updated')
            before = list(old_video.objects.order_by('id').values(*retained_fields))

            executor = MigrationExecutor(connection)
            executor.migrate(self.migrate_to)
            new_apps = executor.loader.project_state(self.migrate_to).apps
            video = new_apps.get_model('video', 'Video')

            self.assertEqual(len(records), video.objects.count())
            self.assertEqual(before, list(video.objects.order_by('id').values(*retained_fields)))
            self.assertNotIn('video_videocategory', connection.introspection.table_names())
            with connection.cursor() as cursor:
                columns = {column.name for column in connection.introspection.get_table_description(cursor, 'video_video')}
            self.assertTrue({'category', 'tags', 'youtube_status'}.isdisjoint(columns))
        finally:
            MigrationExecutor(connection).migrate(final_targets)

    def test_migration_does_not_silently_publish_previously_hidden_video_links(self):
        executor = MigrationExecutor(connection)
        final_targets = executor.loader.graph.leaf_nodes()
        executor.migrate(self.migrate_from)
        old_apps = executor.loader.project_state(self.migrate_from).apps
        video = old_apps.get_model('video', 'Video')
        try:
            for status in (None, 0, 1):
                with self.subTest(status=status):
                    record = video.objects.create(
                        caption='Hidden linked video', youtube_id='qH6i5JsntCw',
                        youtube_status=status, file='youtube/original.wmv',
                    )
                    with self.assertRaisesRegex(RuntimeError, 'hidden videos already have a YouTube ID'):
                        MigrationExecutor(connection).migrate(self.migrate_to)
                    record.refresh_from_db()
                    self.assertEqual(record.youtube_id, 'qH6i5JsntCw')
                    self.assertEqual(record.youtube_status, status)
                    self.assertIn('video_videocategory', connection.introspection.table_names())
                    record.delete()
        finally:
            video.objects.filter(caption='Hidden linked video').delete()
            MigrationExecutor(connection).migrate(final_targets)
