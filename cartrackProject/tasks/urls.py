from django.urls import path
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from . import views

app_name = 'mytasks'
urlpatterns = [
    path('task/', views.task, name='task'),
    path('testDetect/', views.testDetect, name='testDetect'),
    path('upload/', views.upload_video, name='upload_video'),
    path('videoDetect/<int:video_id>', views.videoDetect, name='videoDetect'),
    path('setloopview/<int:id>', views.set_loop_view, name="set_loop_view"),
    path('setloop/<int:id>',views.set_loop, name='set_loop'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)