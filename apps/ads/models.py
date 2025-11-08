from apps.categories.models import Category
from apps.video.models import Video
from django.db import models
from ckeditor.fields import RichTextField

class AdBlock(models.Model):
    CONTENT_TYPE_CHOICES = [
        ('video', 'Video'),
        ('category', 'Category'),
    ]
    
    title = models.CharField(max_length=200)
    description = RichTextField(blank=True, help_text="Ad block description with rich text formatting")
    background_image = models.ImageField(upload_to='ads/', blank=True, null=True, help_text="Background image for the ad block")
    content_type = models.CharField(
        max_length=20,
        choices=CONTENT_TYPE_CHOICES,
        default='category',
        help_text="Type of content this ad block links to"
    )
    video = models.ForeignKey(
        Video,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='ad_blocks',
        help_text="Video to link to (if content_type is 'video')"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='ad_blocks',
        help_text="Category to link to (if content_type is 'category')"
    )
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0, help_text="Display order on homepage")
    
    # SEO/OpenGraph fields
    meta_title = models.CharField(max_length=60, blank=True, help_text="SEO title (60 characters max)")
    meta_description = models.CharField(max_length=160, blank=True, help_text="SEO description (160 characters max)")
    meta_keywords = models.CharField(max_length=255, blank=True, help_text="SEO keywords separated by commas")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Advertising Block"
        verbose_name_plural = "Advertising Blocks"
    
    def __str__(self):
        return str(self.title)
    
    def get_link(self):
        """Returns the appropriate link based on content_type"""
        if self.content_type == 'video' and self.video:
            return f"/mobile/videos/{self.video.id}/"
        elif self.content_type == 'category' and self.category:
            return f"/mobile/categories/{self.category.slug}/"
        return "#"