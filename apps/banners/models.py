from apps.categories.models import Category
from django.db import models
from ckeditor.fields import RichTextField

class Banner(models.Model):
    title = models.CharField(max_length=200)
    description = RichTextField(blank=True, help_text="Banner description with rich text formatting")
    image = models.ImageField(upload_to='banners/')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Category to navigate to when banner is clicked"
    )
    external_link = models.URLField(
        blank=True,
        null=True,
        help_text="External URL (if not using category)"
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
    
    def __str__(self):
        return str(self.title)
    
    def get_link(self):
        """Returns the appropriate link based on category or external_link"""
        if self.category:
            return f"/mobile/categories/{self.category.slug}/"
        return self.external_link or "#"