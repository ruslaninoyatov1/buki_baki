# Migration to fix created_at field
from django.db import migrations, models
from django.utils import timezone


def set_created_at_for_existing_records(apps, schema_editor):
    """Set created_at for existing records"""
    Banner = apps.get_model('banners', 'Banner')
    Banner.objects.filter(created_at__isnull=True).update(created_at=timezone.now())


class Migration(migrations.Migration):

    dependencies = [
        ('banners', '0002_update_banner_fields'),
    ]

    operations = [
        migrations.RunPython(set_created_at_for_existing_records, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='banner',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]

