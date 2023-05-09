from django.urls import path
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from . import views

app_name = 'mytasks'
urlpatterns = [

    path('task/', views.task, name='task'),
    path('upload/', views.upload_video, name='upload_video'),
    path('statistic/', views.statistic, name='statistic'),
    path('detect/<int:task_id>', views.detect, name='detect'),
    path('task/<int:task_id>/loop', views.loop_dashboard, name='loop_dashboard'),
    path('loop/new/<int:task_id>', views.new_loop, name='new_loop'),
    path('loop/edit/<int:loop_id>/', views.edit_loop, name='edit_loop'),
    path('loop/delete/<int:loop_id>/', views.delete_loop, name='delete_loop'),
    path('counting_result_file/<int:task_id>/', views.counting_result_file, name="counting_result_file"),
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
