from apps.categories.models import Category
from django.db import models
from ckeditor.fields import RichTextField

class Task(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    AGE_GROUP_CHOICES = [
        ('3-5', '3-5 years'),
        ('6-8', '6-8 years'),
        ('9-12', '9-12 years'),
    ]
    
    title = models.CharField(max_length=200)
    description = RichTextField(blank=True, help_text="Task description with rich text formatting")
    preview = models.ImageField(upload_to='tasks/previews/', help_text="Preview image (JPEG/PNG)")
    file = models.FileField(upload_to='tasks/files/', help_text="PDF file")
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    age_group = models.CharField(max_length=10, choices=AGE_GROUP_CHOICES)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    # SEO/OpenGraph fields
    meta_title = models.CharField(max_length=60, blank=True, help_text="SEO title (60 characters max)")
    meta_description = models.CharField(max_length=160, blank=True, help_text="SEO description (160 characters max)")
    meta_keywords = models.CharField(max_length=255, blank=True, help_text="SEO keywords separated by commas")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
    
    def __str__(self):
        return str(self.title)