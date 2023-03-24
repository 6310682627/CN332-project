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