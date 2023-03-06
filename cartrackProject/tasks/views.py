from django.shortcuts import render
from .tasks import Detect, Opt

def testDetect(request):
    opt = Opt()
    opt.source = "./videos_uploaded/videoKodShort.mp4"
    d = Detect(opt)
    return render(request, 'tasks/testDetect.html', {
        'd': d,
    })