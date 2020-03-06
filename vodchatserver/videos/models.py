import uuid
from django.db import models
from django.utils.timezone import now

class Video(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=256)
    description = models.CharField(max_length=4096)
    date_created = models.DateTimeField(default=now, editable=False)
    videofile = models.FileField(upload_to='videos/', null=True, verbose_name='')

class VideoThumbnail(models.Model):
    video_id = models.ForeignKey(Video, on_delete=models.CASCADE)
