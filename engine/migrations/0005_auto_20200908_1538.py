# Generated by Django 3.0.8 on 2020-09-08 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0004_auto_20200908_1258'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='IMDb',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='length',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='other_names',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
