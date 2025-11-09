from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField

class Category(models.Model):
    CATEGORY_TYPES = [
        ('coloring', _('Раскраски')),
        ('tasks', _('Задания')),
        ('videos', _('Видео уроки')),
    ]
    
    title = models.CharField(max_length=200)
    description = RichTextField(blank=True, help_text="Category description with rich text formatting")
    category_type = models.CharField(
        max_length=20,
        choices=CATEGORY_TYPES,
        default='coloring',
        help_text="Select the type of content this category belongs to"
    )
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
        # Get the display value for category_type
        category_type_display = ""
        for choice in self.CATEGORY_TYPES:
            if choice[0] == self.category_type:
                category_type_display = choice[1]
                break
        return f"{self.title} ({category_type_display}) {'(Free)' if self.is_free else ''}"