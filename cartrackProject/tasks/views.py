from django.shortcuts import render
from .tasks import Detect, Opt
from .models import *

def testDetect(request):
    opt = Opt()
    source_path = "videos_uploaded/"
    source_name = "VideoKodShort.mp4"
    target_path = "videos_tracking/object_tracking/"
    opt.source = f"{source_path}{source_name}"
    d = Detect(opt)
    my_files = OriginalVideo.objects.filter(video__contains=f"{source_path}{source_name}")
    TrackingVideo.objects.create(
        original = my_files.first(),
        video = f"{target_path}{source_name}",
    )
    return render(request, 'tasks/testDetect.html', {
        'd': d,
    })