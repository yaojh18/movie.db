# Generated by Django 3.0.8 on 2020-09-09 17:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0010_auto_20200909_1355'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='image_url',
        ),
    ]
