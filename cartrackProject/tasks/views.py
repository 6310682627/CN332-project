from django.shortcuts import render
from .tasks import Detect, Opt
from django.http import HttpResponse
from .models import OriginalVideo, TrackingVideo
from django.contrib.auth.models import User

def testDetect(request):
    opt = Opt()
    opt.source = "./videos_uploaded/videoKodShort.mp4"
    d = Detect(opt)
    return render(request, 'tasks/testDetect.html', {
        'd': d,
    })


def videoDetect(request,video_id):
	opt = Opt()
	video = OriginalVideo.objects.get(id=video_id).video
	TrackingVideo.objects.create(
		original = OriginalVideo.objects.get(id=video_id), 
		video = "videos_tracking/object_tracking/" + video.name.split('/')[1]
		)
	video_name = 'videos_tracking/object_tracking/' + video.name.split('/')[1]
	opt.source = video.path 
	d = Detect(opt)
	return render(request, 'tasks/videoDetect.html', {
        'd': d,
		'video_name':video_name
    })

def upload_video(request):
	name_track = []
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