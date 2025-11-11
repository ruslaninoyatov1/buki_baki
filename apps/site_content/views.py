from django.shortcuts import render
from .models import SiteContent

def get_site_content():
    """Get the site content, creating a default if none exists"""
    site_content = SiteContent.objects.first()
    if not site_content:
        # Create default content
        site_content = SiteContent.objects.create()
    return site_content