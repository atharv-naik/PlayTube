# Generated by Django 4.1.2 on 2023-06-08 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('play', '0015_alter_video_genre'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='video_file',
            field=models.FileField(null=True, upload_to='videos/'),
        ),
    ]