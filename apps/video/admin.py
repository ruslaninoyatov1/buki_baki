from django.contrib import admin
from .models import Video, VideoSeries
from ckeditor.widgets import CKEditorWidget
from django import forms

@admin.register(VideoSeries)
class VideoSeriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name',)
    readonly_fields = ('created_at',)


class VideoAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget(), required=False)
    
    class Meta:
        model = Video
        fields = '__all__'


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    form = VideoAdminForm
    list_display = ('title', 'category', 'is_series', 'series_group', 'order', 'date')
    list_filter = ('category', 'is_series', 'date')
    search_fields = ('title', 'description')
    readonly_fields = ('date',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'category')
        }),
        ('Video File', {
            'fields': ('file', 'preview'),
            'description': 'Upload MP4 video file and preview image'
        }),
        ('Series Options', {
            'fields': ('is_series', 'series_group', 'order'),
            'description': 'Check "Is series" if this video is part of a series, then select the series group'
        }),
        ('Timestamps', {
            'fields': ('date',),
            'classes': ('collapse',)
        }),
    )