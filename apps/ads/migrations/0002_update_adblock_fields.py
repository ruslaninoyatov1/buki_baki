# Generated migration to update AdBlock model
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0001_initial'),
        ('categories', '0001_initial'),
        ('video', '0001_initial'),
    ]

    operations = [
        # Step 1: Rename image to background_image (allowing null temporarily)
        migrations.RenameField(
            model_name='adblock',
            old_name='image',
            new_name='background_image',
        ),
        # Step 2: Make background_image nullable temporarily
        migrations.AlterField(
            model_name='adblock',
            name='background_image',
            field=models.ImageField(blank=True, null=True, upload_to='ads/'),
        ),
        # Step 3: Remove old fields (link, position)
        migrations.RemoveField(
            model_name='adblock',
            name='link',
        ),
        migrations.RemoveField(
            model_name='adblock',
            name='position',
        ),
        # Step 4: Add new fields
        migrations.AddField(
            model_name='adblock',
            name='content_type',
            field=models.CharField(choices=[('video', 'Video'), ('category', 'Category')], default='category', max_length=20),
        ),
        migrations.AddField(
            model_name='adblock',
            name='video',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ad_blocks', to='video.video'),
        ),
        migrations.AddField(
            model_name='adblock',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ad_blocks', to='categories.category'),
        ),
        migrations.AddField(
            model_name='adblock',
            name='order',
            field=models.IntegerField(default=0, help_text='Display order on homepage'),
        ),
        migrations.AddField(
            model_name='adblock',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        # Step 5: Make background_image required again (after migration)
        # This will be done in a follow-up migration if needed
    ]

