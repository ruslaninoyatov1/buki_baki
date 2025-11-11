from django.contrib import admin
from .models import SiteContent

@admin.register(SiteContent)
class SiteContentAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    fieldsets = (
        ('Home Page Content', {
            'fields': ('home_page_title', 'home_page_subtitle', 'home_page_description', 'home_page_button_text')
        }),
        ('Most Popular Section', {
            'fields': ('most_popular_title', 'most_popular_description')
        }),
        ('Features Section', {
            'fields': ('features_section_title',)
        }),
        ('Presentation Section', {
            'fields': ('presentation_title',)
        }),
        ('Color Customization', {
            'fields': ('primary_color', 'secondary_color', 'accent_color')
        }),
        ('SEO Settings', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords')
        }),
    )