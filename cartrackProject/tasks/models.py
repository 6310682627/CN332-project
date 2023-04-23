from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
from datetime import datetime

class OriginalVideo(models.Model):
    video = models.FileField(upload_to='videos_uploaded', null=True, validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])])
    

    def __str__(self):
        return f"{self.video}"
    

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task_id = models.AutoField(primary_key=True)
    task_name = models.CharField(max_length=200)
    date_time = models.DateField(default=datetime.now)
    date_time_modify = models.DateTimeField(auto_now=True)
    date_time_upload = models.DateTimeField(auto_now_add=True)
    OriginalVideo = models.OneToOneField(
        OriginalVideo,
        on_delete=models.CASCADE,
    )
    video_result_file = models.FileField(upload_to='result/video/', null=True)
    counting_result_file = models.FileField(upload_to='result/counting/', null=True)
    

class Loop(models.Model):
    head_task = models.ForeignKey(Task, on_delete=models.CASCADE)
    loop_name = models.CharField(max_length=255)
    loop_id = models.IntegerField()
    orientation = models.CharField(max_length=255)
    x1 = models.IntegerField()
    y1 = models.IntegerField()
    x2 = models.IntegerField()
    y2 = models.IntegerField()
    x3 = models.IntegerField()
    y3 = models.IntegerField()
    x4 = models.IntegerField()
    y4 = models.IntegerField()
    summary_location_x = models.IntegerField()
    summary_location_y = models.IntegerField()
    