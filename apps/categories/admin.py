from django.contrib import admin
from .models import Category
from ckeditor.widgets import CKEditorWidget
from django import forms


class CategoryAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget(), required=False)
    
    class Meta:
        model = Category
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm
    list_display = ('title', 'category_type', 'slug', 'is_free')
    list_filter = ('category_type', 'is_free',)
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'category_type', 'slug', 'is_free'),
            'description': 'Mark category as "Free" to make it accessible without subscription'
        }),
    )