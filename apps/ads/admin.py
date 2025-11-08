from django.contrib import admin
from .models import AdBlock
from ckeditor.widgets import CKEditorWidget
from django import forms


class AdBlockAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget(), required=False)
    
    class Meta:
        model = AdBlock
        fields = '__all__'


@admin.register(AdBlock)
class AdBlockAdmin(admin.ModelAdmin):
    form = AdBlockAdminForm
    list_display = ('title', 'content_type', 'video', 'category', 'order', 'is_active', 'created_at')
    list_filter = ('content_type', 'is_active', 'created_at')
    search_fields = ('title',)
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'background_image')
        }),
        ('Content Link', {
            'fields': ('content_type', 'video', 'category'),
            'description': 'Select content type (video or category) and choose the specific content to link to'
        }),
        ('Display Options', {
            'fields': ('order', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )