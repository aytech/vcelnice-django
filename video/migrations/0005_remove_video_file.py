from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0004_remove_youtube_upload_workflow'),
    ]

    operations = [
        migrations.RemoveField(model_name='video', name='file'),
    ]
