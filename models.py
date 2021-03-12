from django.db import models

# Create your models here.


class NewsStories(models.Model):
    headline = models.CharField(max_length=64)
    Storycategory=[('pol','politics'),('art','art'),('tech','technology'),('trivia','triva news')]
    category = models.CharField(max_length=32,choices=Storycategory,default='unknown')
    regions=[('uk','uk'),('eu','european news'),('w','world news')]
    region=models.CharField(max_length=10,choices=regions,default='unknown')
    author = models.CharField(max_length=100)
    date=models.DateTimeField(auto_now_add=True)
    details=models.CharField(max_length=512)

    def __str__(self):
        return self.headline

class Author(models.Model):
    username=models.CharField(max_length=30, unique=True)
    password=models.CharField(max_length=30)
    name=models.CharField(max_length=30)
    def __str__(self):
        return self.username
