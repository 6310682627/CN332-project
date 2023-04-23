from celery import shared_task
from detect_and_track import engine
from tasks.models import Task, Loop
import os


@shared_task
def detect_celery(vdofile, loopfile, task_id):
    saved_result = engine(loopfile, cmd=False, custom_arg=[
                          '--source', vdofile])
    counting_result_path, video_result_path = saved_result
    task = Task.objects.get(pk=task_id)
    counting_result_file = open(counting_result_path, 'rb')
    video_file = open(video_result_path, 'rb')
    task.video_result_file.save(f"{task_id}.mp4", video_file, save=True)
    task.counting_result_file.save(
        f"{task_id}.txt", counting_result_file, save=True)
    task.save()
    counting_result_file.close()
    video_file.close()

    return saved_result