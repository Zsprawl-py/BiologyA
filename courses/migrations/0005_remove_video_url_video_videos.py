# Generated by Django 4.2.7 on 2024-01-05 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_alter_content_content_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='url',
        ),
        migrations.AddField(
            model_name='video',
            name='videos',
            field=models.FileField(blank=True, null=True, upload_to='videos'),
        ),
    ]
