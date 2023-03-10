from __future__ import absolute_import, unicode_literals
from celery import shared_task
import torch
import sys

sys.path.append('./arial-car-track')
import detect
from .models import *

class Opt:
    
    weights = './arial-car-track/yolov7.pt'
    download = True
    no_download = False
    source = 'inference/images'
    img_size = 640
    conf_thres = 0.25
    iou_thres = 0.45
    device = ''
    view_img = False
    save_txt = False
    save_conf = True
    nosave = False
    classes = 0
    agnostic_nms = True
    augment = True
    update = True
    project = 'videos_tracking'
    name = 'object_tracking'
    exist_ok = True
    no_trace = True


@shared_task
def Detect(opt):
    with torch.no_grad():
        d = detect.Detector(opt)
        d.run(opt)
    my_files = OriginalVideo.objects.filter(video__contains=f"videos_uploaded/VideoKodShort.mp4")
    TrackingVideo.objects.create(
        original = my_files.first(),
        video = f"videos_tracking/object_tracking/VideoKodShort.mp4",
    )
    
    return "finish!"
    