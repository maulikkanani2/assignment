from operator import mod
from statistics import mode
from django.db import models

class Assignment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    music_genre = models.CharField(max_length=255)
    daily_practice_time = models.IntegerField()
    days = models.IntegerField()
    days_practiced = models.IntegerField()
    base = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.title