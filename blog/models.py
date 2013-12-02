from django.db import models

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    publish_date = models.DateField()
    comments_count = models.IntegerField(default=0)
    slug = models.SlugField(max_length=100, null=True, blank=True)

    def __unicode__(self):
        return self.title


class Comment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.CharField(max_length=100)
    comment_date = models.DateField()
    post = models.ForeignKey(Post)

    def __unicode__(self):
        return self.content
