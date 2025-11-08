from apps.categories.models import Category
from django.db import models
from ckeditor.fields import RichTextField

class Coloring(models.Model):
    title = models.CharField(max_length=200)
    description = RichTextField(blank=True, help_text="Coloring description with rich text formatting")
    preview = models.ImageField(upload_to='coloring/previews/', help_text="Preview image (JPEG/PNG)")
    file = models.FileField(upload_to='coloring/files/', help_text="PDF file")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    # SEO/OpenGraph fields
    meta_title = models.CharField(max_length=60, blank=True, help_text="SEO title (60 characters max)")
    meta_description = models.CharField(max_length=160, blank=True, help_text="SEO description (160 characters max)")
    meta_keywords = models.CharField(max_length=255, blank=True, help_text="SEO keywords separated by commas")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Coloring"
        verbose_name_plural = "Colorings"
    
    def __str__(self):
        return str(self.title)