from django.urls import path
from . import views

app_name = 'mytasks'
urlpatterns = [
    path('testDetect/', views.testDetect, name='testDetect'),
] 