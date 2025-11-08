# Generated migration to add created_at field to Coloring
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coloring', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='coloring',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]

