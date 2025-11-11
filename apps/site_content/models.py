from django.db import models
from ckeditor.fields import RichTextField

class SiteContent(models.Model):
    # Home page content
    home_page_title = models.CharField(max_length=200, default="Work faster with powerful tools")
    home_page_subtitle = models.CharField(max_length=200, default="trendy application")
    home_page_description = RichTextField(blank=True, default="Laboris culpa ea incididunt dolore ipsum tempor duis&nbsp;do ullamco eiusmod officia magna ad id.")
    home_page_button_text = models.CharField(max_length=50, default="Learn More")
    
    # Most popular section
    most_popular_title = models.CharField(max_length=200, default="The most popular application 2021")
    most_popular_description = RichTextField(blank=True, default="Culpa non ex tempor qui nulla laborum. Laboris&nbsp;culpa ea incididunt dolore ipsum.")
    
    # Features section
    features_section_title = models.CharField(max_length=200, default="See what you will get with us")
    
    # Presentation section
    presentation_title = models.CharField(max_length=200, default="Watch our UI presentation")
    
    # Color customization
    primary_color = models.CharField(max_length=7, default="#FF6B35", help_text="Primary color in hex format (e.g., #FF6B35)")
    secondary_color = models.CharField(max_length=7, default="#2A363B", help_text="Secondary color in hex format (e.g., #2A363B)")
    accent_color = models.CharField(max_length=7, default="#F0F0F0", help_text="Accent color in hex format (e.g., #F0F0F0)")
    
    # SEO fields
    meta_title = models.CharField(max_length=60, blank=True, help_text="SEO title (60 characters max)")
    meta_description = models.CharField(max_length=160, blank=True, help_text="SEO description (160 characters max)")
    meta_keywords = models.CharField(max_length=255, blank=True, help_text="SEO keywords separated by commas")
    
    class Meta:
        verbose_name_plural = "Site Content"
        
    def __str__(self):
        return "Site Content (Editable Texts)"