from django import forms
from .models import Task, Loop,OriginalVideo
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import DateTimeInput, TimeInput
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.core.validators import FileExtensionValidator

class OriginalVideoForm(forms.ModelForm):
    class Meta:
        model = OriginalVideo
        fields = ['video']
        widgets = {
            'video': forms.FileInput(attrs={'class': 'form-control-file'})
        }
        validators = [FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])]



class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_name',]
        widgets = {
            'task_name': forms.TextInput(attrs={'class': 'form-control'}),
        }



class LoopForm(forms.ModelForm):

    loop_id = forms.IntegerField(validators=[MinValueValidator(0)],widget=forms.TextInput(attrs={'class': 'form-control'}))
    x1 = forms.DecimalField(validators=[MinValueValidator(0)],widget=forms.TextInput(attrs={'class': 'form-control'}))
    y1 = forms.DecimalField(validators=[MinValueValidator(0)],widget=forms.TextInput(attrs={'class': 'form-control'}))
    x2 = forms.DecimalField(validators=[MinValueValidator(0)],widget=forms.TextInput(attrs={'class': 'form-control'}))
    y2 = forms.DecimalField(validators=[MinValueValidator(0)],widget=forms.TextInput(attrs={'class': 'form-control'}))
    x3 = forms.DecimalField(validators=[MinValueValidator(0)],widget=forms.TextInput(attrs={'class': 'form-control'}))
    y3 = forms.DecimalField(validators=[MinValueValidator(0)],widget=forms.TextInput(attrs={'class': 'form-control'}))
    x4 = forms.DecimalField(validators=[MinValueValidator(0)],widget=forms.TextInput(attrs={'class': 'form-control'}))
    y4 = forms.DecimalField(validators=[MinValueValidator(0)],widget=forms.TextInput(attrs={'class': 'form-control'}))
    summary_location_x = forms.DecimalField(validators=[MinValueValidator(0)],widget=forms.TextInput(attrs={'class': 'form-control'}))
    summary_location_y = forms.DecimalField(validators=[MinValueValidator(0)],widget=forms.TextInput(attrs={'class': 'form-control'}))


    class Meta:
        model = Loop
        fields = ['loop_name', 'loop_id', 'orientation',
                  'x1', 'y1', 'x2', 'y2', 'x3', 'y3', 'x4', 'y4',
                  'summary_location_x', 'summary_location_y']
        widgets = {'loop_name' : forms.TextInput(attrs={'class': 'form-control'}), 'orientation' : forms.TextInput(attrs={'class': 'form-control'})}