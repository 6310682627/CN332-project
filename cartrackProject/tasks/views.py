from django.shortcuts import render, reverse, redirect, get_object_or_404
# from tasks import Detect, optJson, Detect_and_Track
from django.http import HttpResponse
from .models import *
from django.contrib.auth.models import User
import cv2
from .forms import TaskForm, LoopForm,OriginalVideoForm

from .tasks import detect_celery

    
        

def upload_video(request):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html')
    else:
        if request.method == 'POST':
            task_form = TaskForm(request.POST, request.FILES)
            original_video_form = OriginalVideoForm(request.POST, request.FILES)
            
            if task_form.is_valid() and original_video_form.is_valid():
                task = task_form.save(commit=False)
                original_video = original_video_form.save(commit=False)
                original_video.save()
                task.user = request.user
                task.OriginalVideo = original_video
                task.save()

                return redirect('mytasks:task')
        else:
            task_form = TaskForm()
            original_video_form = OriginalVideoForm()
            
        context = {
            'task_form': task_form,
            'original_video_form': original_video_form,
        }
        
        return render(request, 'tasks/upload.html', context)

def task(request):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html')
    
    else:
        tasks = Task.objects.all()
        return render(request, 'tasks/task.html', { 'tasks' : tasks
        })
    
def new_loop(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        form = LoopForm(request.POST)
        if form.is_valid():
            loop = form.save(commit=False)
            loop.head_task = task
            loop.save()
            return redirect(reverse("mytasks:loop_dashboard", args=(task_id,)))
    else:
        form = LoopForm(initial={'head_task': task})
    return render(request, 'loop/NewLoop.html', {'form': form, 'task_id': task_id})


def edit_loop(request, loop_id):
    loop = get_object_or_404(Loop, pk=loop_id)
    if request.method == 'POST':
        form = LoopForm(request.POST, instance=loop)
        if form.is_valid():
            form.save()
            return redirect(reverse("mytasks:loop_dashboard", args=(loop.head_task.pk,)))
    else:
        form = LoopForm(instance=loop)
    return render(request, 'loop/EditLoop.html', {'form': form, 'task_id': loop.head_task.pk})


def delete_loop(request, loop_id):

    loop = get_object_or_404(Loop, pk=loop_id)

    loop.delete()

    return redirect(reverse("mytasks:loop_dashboard", args=(loop.head_task.pk,)))


def loop_dashboard(request, task_id):
    loops = Loop.objects.filter(head_task__pk=task_id)
    return render(request, 'loop/LoopDashboard.html', {'loops': loops, 'task_id': task_id})


def loops_to_json(task_id):
    loops = Loop.objects.filter(head_task__pk=task_id)
    loop_list = []
    for loop in loops:
        point_list = [
            {'x': loop.x_1, 'y': loop.y_1},
            {'x': loop.x_2, 'y': loop.y_2},
            {'x': loop.x_3, 'y': loop.y_3},
            {'x': loop.x_4, 'y': loop.y_4},
        ]
        summary_location = {'x': loop.summary_location_x,
                            'y': loop.summary_location_y}

        loop_dict = {
            'name': loop.loop_name,
            'id': loop.loop_id,
            'points': point_list,
            'orientation': loop.orientation,
            'summary_location': summary_location
        }

        loop_list.append(loop_dict)

    response_data = {'loops': loop_list}
    return response_data

def new_loop(request, task_id):

    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        form = LoopForm(request.POST)
        if form.is_valid():
            loop = form.save(commit=False)
            loop.head_task = task
            loop.save()
            return redirect(reverse("mytasks:loop_dashboard", args=(task_id,)))
    else:
        form = LoopForm(initial={'head_task': task})
    return render(request, 'loop/NewLoop.html', {'form': form, 'task_id': task_id})


def edit_loop(request, loop_id):
    loop = get_object_or_404(Loop, pk=loop_id)
    if request.method == 'POST':
        form = LoopForm(request.POST, instance=loop)
        if form.is_valid():
            form.save()
            return redirect(reverse("mytasks:loop_dashboard", args=(loop.head_task.pk,)))
    else:
        form = LoopForm(instance=loop)
    return render(request, 'loop/EditLoop.html', {'form': form, 'task_id': loop.head_task.pk})


def delete_loop(request, loop_id):

    loop = get_object_or_404(Loop, pk=loop_id)

    loop.delete()

    return redirect(reverse("mytasks:loop_dashboard", args=(loop.head_task.pk,)))


def loop_dashboard(request, task_id):
    loops = Loop.objects.filter(head_task__pk=task_id)
    return render(request, 'loop/LoopDashboard.html', {'loops': loops, 'task_id': task_id})


def loops_to_json(task_id):
    loops = Loop.objects.filter(head_task__pk=task_id)
    loop_list = []
    for loop in loops:
        point_list = [
            {'x': loop.x1, 'y': loop.y1},
            {'x': loop.x2, 'y': loop.y2},
            {'x': loop.x3, 'y': loop.y3},
            {'x': loop.x4, 'y': loop.y4},
        ]
        summary_location = {'x': loop.summary_location_x,
                            'y': loop.summary_location_y}

        loop_dict = {
            'name': loop.loop_name,
            'id': loop.loop_id,
            'points': point_list,
            'orientation': loop.orientation,
            'summary_location': summary_location
        }

        loop_list.append(loop_dict)

    response_data = {'loops': loop_list}
    return response_data

def detect(request, task_id):
    loopfile_demo = {
        "loops": [
            {
                "name": "loop1",
                "id": "0",
                "points": [
                    {"x": 900, "y": 600},
                    {"x": 900, "y": 300},
                    {"x": 400, "y": 300},
                    {"x": 400, "y": 600}
                ],
                "orientation": "counterclockwise",
                "summary_location": {"x": 20, "y": "20"}
            },
            {
                "name": "loop2",
                "id": "1",
                "points": [
                    {"x": 280, "y": 450},
                    {"x": 280, "y": 200},
                    {"x": 600, "y": 200},
                    {"x": 600, "y": 450}

                ],
                "orientation": "clockwise",
                "summary_location": {"x": 20, "y": "380"}
            },
            {
                "name": "loop3",
                "id": "2",
                "points": [
                    {"x": 600, "y": 80},
                    {"x": 850, "y": 80},
                    {"x": 900, "y": 600},
                    {"x": 600, "y": 600}

                ],
                "orientation": "clockwise",
                "summary_location": {"x": 950, "y": "20"}
            }
        ]
    }
    task = Task.objects.get(pk=task_id)
    loopfile = loops_to_json(task_id)
    vdofile = task.OriginalVideo.video.url.lstrip('/')
    task_result = detect_celery.delay(vdofile, loopfile, task_id)

    return redirect(reverse("mytasks:task"))
def counting_result_file(request,task_id):
    task = Task.objects.get(task_id=task_id)
    context = {
        'result': list()
    }
    if not task.counting_result_file:
        return HttpResponse("Have no result")
    with open(f"{task.counting_result_file.path}", 'r') as result_file:
        for line in result_file:
            context['result'].append(line.split(','))
    return render(request, 'tasks/counting_result_file.html', context)