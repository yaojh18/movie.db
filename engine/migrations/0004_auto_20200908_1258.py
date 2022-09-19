# Generated by Django 3.0.8 on 2020-09-08 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0003_auto_20200908_0006'),
    ]

    operations = [
        migrations.AddField(
            model_name='actor',
            name='name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='categories',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='country',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='dates',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='diretors',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='language',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='scriptwriters',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
