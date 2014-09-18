from django.db import models
import datetime
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=250)
    body = models.TextField()
    published_date = models.DateTimeField(default=datetime.datetime.now)
    author = models.ForeignKey(User)
    docfile = models.FileField(upload_to='documents/%Y/%m/%d', blank = True, null = True)
    
    def __unicode__(self):
      return self.title

class Comment(models.Model):
     post = models.ForeignKey(Post)
     body = models.CharField(max_length=250)
     published_date = models.DateTimeField(default=datetime.datetime.now)
     author = models.CharField(max_length=250)

     def __unicode__(self):
       return self.body
