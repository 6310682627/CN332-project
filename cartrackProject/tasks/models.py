from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
from datetime import datetime

class OriginalVideo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.FileField(upload_to='videos_uploaded', null=True, validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])])
    date = models.DateField(default=datetime.now)

    def __str__(self):
        return f"original video: {self.video} from: {self.user.username}"
    
class TrackingVideo(models.Model):
    original = models.ForeignKey(OriginalVideo, on_delete=models.CASCADE)
    video = models.FileField(upload_to='videos_tracking', null=True, validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])])

    def __str__(self):
        return f"tracking video: {self.id}"


class Loop(models.Model):
    originalVideo = models.ForeignKey(OriginalVideo, on_delete=models.CASCADE, null=True)
    trackingVideo = models.ForeignKey(TrackingVideo, on_delete=models.CASCADE , null=True)
    x1 = models.IntegerField()
    y1 = models.IntegerField()
    x2 = models.IntegerField()
    y2 = models.IntegerField()
    x3 = models.IntegerField()
    y3 = models.IntegerField()
    x4 = models.IntegerField()
    y4 = models.IntegerField()
    orientation = models.TextField(default="clockwise")
class LoopWrapper(models.Model) :
        loop1 = models.ForeignKey(Loop, on_delete=models.CASCADE, related_name="loop1")
        loop2 = models.ForeignKey(Loop, on_delete=models.CASCADE, related_name="loop2")
        loop3 = models.ForeignKey(Loop, on_delete=models.CASCADE, related_name="loop3")
        loop4 = models.ForeignKey(Loop, on_delete=models.CASCADE, related_name="loop4")
