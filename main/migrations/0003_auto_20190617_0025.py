# Generated by Django 2.2.2 on 2019-06-17 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20190617_0023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='courses',
            field=models.ManyToManyField(blank=True, null=True, to='main.Course'),
        ),
    ]
