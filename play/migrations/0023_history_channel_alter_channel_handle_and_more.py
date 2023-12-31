# Generated by Django 4.1.2 on 2023-08-16 18:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('play', '0022_history_percentage_watched'),
    ]

    operations = [
        migrations.AddField(
            model_name='history',
            name='channel',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='play.channel'),
        ),
        migrations.AlterField(
            model_name='channel',
            name='handle',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='history',
            unique_together={('channel', 'video')},
        ),
        migrations.RemoveField(
            model_name='history',
            name='user',
        ),
    ]
