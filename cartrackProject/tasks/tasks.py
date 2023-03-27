from __future__ import absolute_import, unicode_literals
from celery import shared_task
import torch
import sys
from .models import OriginalVideo, TrackingVideo
from django.shortcuts import render
from django.http import HttpResponse



sys.path.append('./arial-car-track')
import detect

class Opt:
    def __init__(self, optJson):
        self.weights = optJson["weights"]
        self.download = optJson["download"]
        self.no_download = optJson["no_download"]
        self.source = optJson["source"]
        self.img_size = optJson["img_size"]
        self.conf_thres = optJson["conf_thres"]
        self.iou_thres = optJson["iou_thres"]
        self.device = optJson["device"]
        self.view_img = optJson["view_img"]
        self.save_txt = optJson["save_txt"]
        self.save_conf = optJson["save_conf"]
        self.nosave = optJson["nosave"]
        self.classes = optJson["classes"]
        self.agnostic_nms = optJson["agnostic_nms"]
        self.augment = optJson["augment"]
        self.update = optJson["update"]
        self.project = optJson["project"]
        self.name = optJson["name"]
        self.exist_ok = optJson["exist_ok"]
        self.no_trace = optJson["no_trace"]

optJson = {
    "weights": './arial-car-track/yolov7.pt',
    "download": True,
    "no_download": False,
    "source": 'inference/images',
    "img_size": 640,
    "conf_thres": 0.25,
    "iou_thres": 0.45,
    "device": '',
    "view_img": False,
    "save_txt": False,
    "save_conf": True,
    "nosave": False,
    "classes": [0,1,2,3,4,5],
    "agnostic_nms": True,
    "augment": True,
    "update": True,
    "project": 'videos_tracking',
    "name": 'object_tracking',
    "exist_ok": True,
    "no_trace": True,
}


@shared_task
def Detect(optJson):
    opt = Opt(optJson)
    with torch.no_grad():
        d = detect.Detector(opt)
        d.run(opt)
    return str('ok')
