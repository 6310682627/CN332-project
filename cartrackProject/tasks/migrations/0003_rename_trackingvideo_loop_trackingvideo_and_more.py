# Generated by Django 4.2 on 2023-04-21 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_loopwrapper'),
    ]

    operations = [
        migrations.RenameField(
            model_name='loop',
            old_name='TrackingVideo',
            new_name='trackingVideo',
        ),
        migrations.AddField(
            model_name='loop',
            name='orientation',
            field=models.TextField(default='clockwise'),
        ),
    ]