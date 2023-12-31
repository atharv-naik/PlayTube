# Generated by Django 4.1.2 on 2023-05-20 11:08

from django.db import migrations
import shortuuid.django_fields


class Migration(migrations.Migration):

    dependencies = [
        ('play', '0007_alter_channel_channel_id_alter_video_video_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='channel_id',
            field=shortuuid.django_fields.ShortUUIDField(alphabet=None, editable=False, length=22, max_length=22, prefix='', primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='video_id',
            field=shortuuid.django_fields.ShortUUIDField(alphabet=None, editable=False, length=11, max_length=11, prefix='', primary_key=True, serialize=False, unique=True),
        ),
    ]
