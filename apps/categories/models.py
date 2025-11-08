from django.db import models
from ckeditor.fields import RichTextField

class Category(models.Model):
    title = models.CharField(max_length=200)
    description = RichTextField(blank=True, help_text="Category description with rich text formatting")
    slug = models.SlugField(unique=True)
    is_free = models.BooleanField(
        default=False,
        help_text="Free categories are accessible without subscription"
    )
    
    # SEO/OpenGraph fields
    meta_title = models.CharField(max_length=60, blank=True, help_text="SEO title (60 characters max)")
    meta_description = models.CharField(max_length=160, blank=True, help_text="SEO description (160 characters max)")
    meta_keywords = models.CharField(max_length=255, blank=True, help_text="SEO keywords separated by commas")
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['title']
    
    def __str__(self):
        return f"{self.title} {'(Free)' if self.is_free else ''}"