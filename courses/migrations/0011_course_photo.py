# Generated by Django 4.2.7 on 2024-03-03 23:44

import BiologyA.settings.base
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0010_remove_image_files_image_images'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='photo',
            field=models.FileField(blank=True, null=True, storage=BiologyA.settings.base.ImageStorage(), upload_to='course'),
        ),
    ]