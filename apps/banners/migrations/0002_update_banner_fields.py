# Generated migration to update Banner fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('banners', '0001_initial'),
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='categories.category', help_text='Category to navigate to when banner is clicked'),
        ),
        migrations.AddField(
            model_name='banner',
            name='external_link',
            field=models.URLField(blank=True, null=True, help_text='External URL (if not using category)'),
        ),
        migrations.AddField(
            model_name='banner',
            name='order',
            field=models.IntegerField(default=0, help_text='Display order on homepage'),
        ),
        migrations.AddField(
            model_name='banner',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.RemoveField(
            model_name='banner',
            name='link',
        ),
    ]

