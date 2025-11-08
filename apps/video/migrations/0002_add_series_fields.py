# Generated migration to add series fields to Video
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoSeries',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Video Series',
            },
        ),
        migrations.AddField(
            model_name='video',
            name='is_series',
            field=models.BooleanField(default=False, help_text='Check if this video is part of a series'),
        ),
        migrations.AddField(
            model_name='video',
            name='series_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='videos', to='video.videoseries', help_text='Select series group if this video is part of a series'),
        ),
        migrations.AddField(
            model_name='video',
            name='order',
            field=models.IntegerField(default=0, help_text='Order within series'),
        ),
        migrations.AlterField(
            model_name='video',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='file',
            field=models.FileField(upload_to='videos/files/'),
        ),
        migrations.RemoveField(
            model_name='video',
            name='video_url',
        ),
    ]

