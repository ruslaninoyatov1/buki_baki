from django.contrib import admin
from .models import Banner
from ckeditor.widgets import CKEditorWidget
from django import forms


class BannerAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget(), required=False)
    
    class Meta:
        model = Banner
        fields = '__all__'


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    form = BannerAdminForm
    list_display = ('title', 'category', 'external_link', 'order', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title',)
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'image')
        }),
        ('Navigation', {
            'fields': ('category', 'external_link'),
            'description': 'Choose either category or external link for navigation when banner is clicked'
        }),
        ('Display Options', {
            'fields': ('order', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )