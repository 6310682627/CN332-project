from django.shortcuts import render
from .tasks import Detect, optJson, Detect_and_Track
from django.http import HttpResponse
from .models import *
from django.contrib.auth.models import User
import cv2


def testDetect(request):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html')
    
    else:
        opt = optJson
        opt['source'] = "./sample_videos/videos_uploaded/videoShort.mp4"
        opt['name'] = "loop_VideoShort"
        opt['loop'] = "./arial-car-track/loop/loop1counterclockwise.json"
        
        d = Detect_and_Track.delay(opt)
        return render(request, 'tasks/testDetect.html', {
            'd': d,
        })


def videoDetect(request,video_id):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html')
    
    else:
        opt = optJson
        video = OriginalVideo.objects.get(id=video_id).video
        TrackingVideo.objects.create(
            original = OriginalVideo.objects.get(id=video_id), 
            video = "videos_tracking/object_tracking/" + video.name.split('/')[1]
            )
        video_name = 'videos_tracking/object_tracking/' + video.name.split('/')[1]
        opt['source'] = video.path 
        d = Detect.delay(opt)
        return render(request, 'tasks/videoDetect.html', {
            'd': d,
            'video_name':video_name
        })
        


def upload_video(request):

    if not request.user.is_authenticated:
        return render(request, 'users/login.html')
    
    else:
        name_track=[]
        count = []
        if request.method == 'POST':
            video_file = request.FILES['video']
            user = User.objects.get(username=request.user.username)
            original_video = OriginalVideo.objects.create(user=user,video=video_file)

            for i in OriginalVideo.objects.all():
                count.append(i.video.name.split('/')[1])

            for j in TrackingVideo.objects.all():
                name_track.append(j.video.name.split('/')[2])
            
    
            return render(request, 'tasks/upload.html', {
                'upload_success': True,
                'video': original_video,
                'count': count,
                'name_track': name_track,
            })
        else:
            return render(request, 'tasks/upload.html')

def task(request):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html')
    
    else:
        count = []
        name_track = []
        video = OriginalVideo.objects.all()
        id = []
        date = []
        user = []
        test = OriginalVideo.objects.first()

        for i in OriginalVideo.objects.all():
            count.append(i.video.name.split('/')[1])
            id.append([i.video.name.split('/')[1], i.id])
            date.append([i.video.name.split('/')[1], i.date])
            user.append([i.video.name.split('/')[1], i.user])

        for j in TrackingVideo.objects.all():
            name_track.append(j.video.name.split('/')[2])

        return render(request, 'tasks/task.html', {
            'count': count,
            'name_track': name_track,
            'video': video,
            'id': id,
            'date': date,
            'user': user,
            'test': test.video.name,
        })

def set_loop_view(request, id):
    context = {
        "video": f"{OriginalVideo.objects.get(id=id).video.url}",
        "id": id
    }
    return render(request, "tasks/setLoop copy.html", context)


def set_loop(request, id):
    # width: 960px; height: 540px;
    vid = cv2.VideoCapture(OriginalVideo.objects.get(id=id).video.path)
    height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
    width_ratio = width/960
    height_raio = height/540

    def helper(loop):
        p1 = request.POST.getlist(loop)[0].split(',')
        p2 = request.POST.getlist(loop)[1].split(',')
        p3 = request.POST.getlist(loop)[2].split(',')
        p4 = request.POST.getlist(loop)[3].split(',')
        loop = Loop.objects.create(
            x1=int(p1[0]) * width_ratio,
            y1=int(p1[1]) * height_raio,
            x2=int(p2[0]) * width_ratio,
            y2=int(p2[1]) * height_raio,
            x3=int(p3[0]) * width_ratio,
            y3=int(p3[1]) * height_raio,
            x4=int(p4[0]) * width_ratio,
            y4=int(p4[1]) * height_raio,
            orientation=request.POST.get('orientation'),
            originalVideo = OriginalVideo.objects.get(id=id)
        )
        loop.save()
        return loop
    a = []
    if request.method == 'POST':
        
        for i in ('point1', 'point2', 'point3', 'point4'):
            a.append(helper(i))
        LoopWrapper.objects.create(
            loop1=a[0],
            loop2=a[1],
            loop3=a[2],
            loop4=a[3],
        ).save()
        return HttpResponse('success')

