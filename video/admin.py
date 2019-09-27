from django.contrib import admin
from django.contrib import messages
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from vcelnice.settings import *
from .forms import VideoForm
from .models import Video


class VideoAdmin(admin.ModelAdmin):
    form = VideoForm
    list_display = ['caption', 'created', 'youtube']
    fields = ('caption', 'description', 'file', 'thumb', 'category', 'tags', 'youtube')
    readonly_fields = ('youtube',)

    @staticmethod
    def youtube(obj):
        if obj.id is None:
            return format_html('<strong>%s</strong>' % _('Not ready'))
        if obj.youtube_status == YOUTUBE_STATUS_UPLOADED:
            return format_html('<strong>%s</strong>' % _('Uploaded'))
        if obj.youtube_status == YOUTUBE_STATUS_PENDING_UPDATE:
            return format_html('<strong>%s</strong>' % _('Scheduled for update'))
        if obj.youtube_status == YOUTUBE_STATUS_PENDING_UPLOAD:
            return format_html('<strong>%s</strong>' % _('Scheduled for upload'))
        if obj.youtube_status == YOUTUBE_STATUS_PENDING_DELETE:
            return format_html('<strong>%s</strong>' % _('Scheduled for deletion'))

    def delete_model(self, request, obj):
        not_deleted = obj.youtube_status != YOUTUBE_STATUS_DELETED
        uploaded = obj.youtube_status > YOUTUBE_STATUS_PENDING_UPLOAD

        if not_deleted and uploaded:
            messages.set_level(request, messages.WARNING)
            messages.warning(request, _('Video deletion has been scheduled'))

        super(VideoAdmin, self).delete_model(request, obj)

    def save_model(self, request, obj, form, change):
        if obj.youtube_status > YOUTUBE_STATUS_PENDING_UPLOAD:
            messages.set_level(request, messages.WARNING)
            messages.warning(request, _(
                'Only metadata will be updated on Youtube. To update video, remove and recreate the item'))
        super(VideoAdmin, self).save_model(request, obj, form, change)


admin.site.register(Video, VideoAdmin)
