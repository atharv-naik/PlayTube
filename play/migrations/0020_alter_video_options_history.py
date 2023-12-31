# Generated by Django 4.1.2 on 2023-07-30 16:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import shortuuid.main


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('play', '0019_alter_video_video_file'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='video',
            options={'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.UUIDField(default=shortuuid.main.ShortUUID.uuid, editable=False, primary_key=True, serialize=False, unique=True)),
                ('timestamp', models.IntegerField(default=0)),
                ('last_viewed', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='play.video')),
            ],
            options={
                'ordering': ['-last_viewed'],
            },
        ),
    ]
