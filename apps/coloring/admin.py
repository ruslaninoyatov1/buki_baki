from django.contrib import admin
from .models import Coloring
from ckeditor.widgets import CKEditorWidget
from django import forms


class ColoringAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget(), required=False)
    
    class Meta:
        model = Coloring
        fields = '__all__'


@admin.register(Coloring)
class ColoringAdmin(admin.ModelAdmin):
    form = ColoringAdminForm
    list_display = ('title', 'category', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title',)
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'category')
        }),
        ('Files', {
            'fields': ('preview', 'file'),
            'description': 'Upload preview image (JPEG/PNG) and PDF file'
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )