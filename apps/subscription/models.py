from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from ckeditor.fields import RichTextField

class Subscription(models.Model):
    PLAN_CHOICES = [
        ('basic', 'Basic'),
        ('popular', 'Popular'),
    ]
    
    PAYMENT_PLATFORM_CHOICES = [
        ('google_play', 'Google Play'),
        ('app_store', 'Apple App Store'),
        ('web', 'Web Payment'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES)
    description = RichTextField(blank=True, help_text="Subscription plan description with rich text formatting")
    payment_platform = models.CharField(
        max_length=20,
        choices=PAYMENT_PLATFORM_CHOICES,
        default='web'
    )
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    
    # SEO/OpenGraph fields
    meta_title = models.CharField(max_length=60, blank=True, help_text="SEO title (60 characters max)")
    meta_description = models.CharField(max_length=160, blank=True, help_text="SEO description (160 characters max)")
    meta_keywords = models.CharField(max_length=255, blank=True, help_text="SEO keywords separated by commas")
    
    # Payment integration fields
    google_play_order_id = models.CharField(max_length=255, blank=True, null=True)
    app_store_transaction_id = models.CharField(max_length=255, blank=True, null=True)
    purchase_token = models.CharField(max_length=500, blank=True, null=True)  # For Google Play
    receipt_data = models.TextField(blank=True, null=True)  # For App Store
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.plan} ({self.payment_platform})"
    
    @property
    def is_valid(self):
        """Check if subscription is currently valid"""
        now = timezone.now()
        return self.is_active and self.start_date <= now <= self.end_date
    
    def renew(self, months=1):
        """Extend subscription by specified months"""
        if self.end_date < timezone.now():
            self.start_date = timezone.now()
            # Add months using timedelta (approximate, 30 days per month)
            days = months * 30
            self.end_date = self.start_date + timedelta(days=days)
        else:
            # Add months to existing end_date
            days = months * 30
            self.end_date = self.end_date + timedelta(days=days)
        self.is_active = True
        self.save()