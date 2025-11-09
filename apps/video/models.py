from apps.categories.models import Category
from django.db import models
from ckeditor.fields import RichTextField

class VideoSeries(models.Model):
    """Series group for videos"""
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.name)
    
    class Meta:
        verbose_name_plural = "Video Series"

class Video(models.Model):
    title = models.CharField(max_length=200)
    description = RichTextField(blank=True, help_text="Video description with rich text formatting")
    preview = models.ImageField(upload_to='videos/previews/')
    large_preview = models.FileField(
        upload_to='videos/large_previews/', 
        blank=True, 
        null=True,
        help_text="Large preview file (MP4 or other video format)"
    )
    file = models.FileField(upload_to='videos/files/')  # MP4 file required
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_series = models.BooleanField(default=False, help_text="Check if this video is part of a series")
    series_group = models.ForeignKey(
        VideoSeries, 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True,
        related_name='videos',
        help_text="Select series group if this video is part of a series"
    )
    order = models.IntegerField(default=0, help_text="Order within series")
    
    # SEO/OpenGraph fields
    meta_title = models.CharField(max_length=60, blank=True, help_text="SEO title (60 characters max)")
    meta_description = models.CharField(max_length=160, blank=True, help_text="SEO description (160 characters max)")
    meta_keywords = models.CharField(max_length=255, blank=True, help_text="SEO keywords separated by commas")
    
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['series_group', 'order', '-date']
        verbose_name = "Video"
        verbose_name_plural = "Videos"
    
    def __str__(self):
        if self.is_series and self.series_group:
            return f"{self.title} ({self.series_group.name})"
        return str(self.title)