from django.contrib import admin
from .models import Task
from ckeditor.widgets import CKEditorWidget
from django import forms


class TaskAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget(), required=False)
    
    class Meta:
        model = Task
        fields = '__all__'


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    form = TaskAdminForm
    list_display = ('title', 'category', 'difficulty', 'age_group', 'created_at')
    list_filter = ('category', 'difficulty', 'age_group', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'category')
        }),
        ('Task Details', {
            'fields': ('difficulty', 'age_group')
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