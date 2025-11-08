# Generated migration to add is_free field to Category
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='is_free',
            field=models.BooleanField(default=False, help_text='Free categories are accessible without subscription'),
        ),
    ]

