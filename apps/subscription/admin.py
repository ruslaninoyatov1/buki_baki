from django.contrib import admin
from django.utils import timezone
from .models import Subscription
from ckeditor.widgets import CKEditorWidget
from django import forms


class SubscriptionAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget(), required=False)
    
    class Meta:
        model = Subscription
        fields = '__all__'


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    form = SubscriptionAdminForm
    list_display = ('user', 'plan', 'payment_platform', 'start_date', 'end_date', 'is_valid', 'is_active', 'created_at')
    list_filter = ('plan', 'payment_platform', 'is_active', 'created_at')
    search_fields = ('user__username', 'google_play_order_id', 'app_store_transaction_id')
    readonly_fields = ('created_at', 'updated_at', 'is_valid')
    actions = ['activate_subscriptions', 'deactivate_subscriptions', 'extend_subscriptions_30_days']
    fieldsets = (
        ('User & Plan', {
            'fields': ('user', 'plan', 'description')
        }),
        ('Payment Information', {
            'fields': ('payment_platform', 'google_play_order_id', 'app_store_transaction_id', 'purchase_token', 'receipt_data')
        }),
        ('Subscription Dates', {
            'fields': ('start_date', 'end_date', 'is_active', 'is_valid')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def is_valid(self, obj):
        return obj.is_valid
    is_valid.boolean = True
    is_valid.short_description = 'Valid Now'
    
    def activate_subscriptions(self, request, queryset):
        """Activate selected subscriptions"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} subscription(s) activated successfully.")
    activate_subscriptions.short_description = "Activate selected subscriptions"
    
    def deactivate_subscriptions(self, request, queryset):
        """Deactivate selected subscriptions"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} subscription(s) deactivated successfully.")
    deactivate_subscriptions.short_description = "Deactivate selected subscriptions"
    
    def extend_subscriptions_30_days(self, request, queryset):
        """Extend selected subscriptions by 30 days"""
        count = 0
        for subscription in queryset:
            subscription.renew(months=1)  # 1 month = 30 days
            count += 1
        self.message_user(request, f"{count} subscription(s) extended by 30 days.")
    extend_subscriptions_30_days.short_description = "Extend selected subscriptions by 30 days"