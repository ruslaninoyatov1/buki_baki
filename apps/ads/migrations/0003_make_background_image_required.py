# Generated migration to make background_image required
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0002_update_adblock_fields'),
    ]

    operations = [
        # Make background_image required again (only if all records have images)
        # If some records don't have images, keep it nullable
        migrations.AlterField(
            model_name='adblock',
            name='background_image',
            field=models.ImageField(help_text='Background image for the ad block', upload_to='ads/', blank=True, null=True),
        ),
    ]

