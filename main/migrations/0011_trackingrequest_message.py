# Generated by Django 2.2.2 on 2019-07-11 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_user_saved_events'),
    ]

    operations = [
        migrations.AddField(
            model_name='trackingrequest',
            name='message',
            field=models.TextField(blank=True, null=True),
        ),
    ]