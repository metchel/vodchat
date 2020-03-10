import uuid
from django.conf import settings
from django.db import models
from django.utils.timezone import now

class Video(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=256)
    description = models.CharField(max_length=4096)
    date_created = models.DateTimeField(default=now, editable=False)
    videofile = models.FileField(upload_to='videos/', null=True, verbose_name='')

class Thumbnail(models.Model):
    video_id = models.ForeignKey(Video, on_delete=models.CASCADE)
    imagefile = models.FileField(upload_to='thumbnails/', null=True, verbose_name='')

class Comment(models.Model):
    video_id = models.ForeignKey(Video, on_delete=models.CASCADE)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    text = models.CharField(max_length=4096)
    timestamp = models.FloatField(default=0.0)

class Vote(models.Model):
    video_id = models.ForeignKey(Video, on_delete=models.CASCADE)
    voter = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    comment_id = models.ForeignKey(Comment, on_delete=models.CASCADE)
    vote = models.IntegerField(default=0)
