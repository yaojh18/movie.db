from django.db import models

# Create your models here.

class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=100)
    rate = models.FloatField()
    title = models.CharField(max_length=100, null=True)
    summary = models.CharField(max_length=6000, null=True)

    diretors = models.CharField(max_length=200, null=True)
    scriptwriters = models.CharField(max_length=200, null=True)
    categories = models.CharField(max_length=200, null=True)
    dates = models.CharField(max_length=200, null=True)
    language = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=True)
    other_names = models.CharField(max_length=100, null=True)
    length = models.CharField(max_length=100, null=True)
    IMDb = models.CharField(max_length=100, null=True)



class Actor(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=100)
    name = models.CharField(max_length=100, null=True)
    eng_name = models.CharField(max_length=100, null=True)
    movies = models.ManyToManyField('Movie', related_name='actors')

    gender = models.CharField(max_length=100, null=True)
    star_sign = models.CharField(max_length=100, null=True)
    birth_date = models.CharField(max_length=100, null=True)
    birth_place = models.CharField(max_length=100, null=True)
    occupation = models.CharField(max_length=100, null=True)
    other_names = models.CharField(max_length=200, null=True)
    families = models.CharField(max_length=200, null=True)
    summary = models.CharField(max_length=6000, null=True)
    IMDb = models.CharField(max_length=100, null=True)
    has_img = models.BooleanField(null=True)
    colleague = models.CharField(max_length=100, null=True)

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=2000, null=True)
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE, related_name='comments')
