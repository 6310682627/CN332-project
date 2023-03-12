from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from .forms import SignUpForm, UpdateUserForm

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('users:login'))
    return render(request,"users/index.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('users:index'))
        else:
            return render(request, "users/login.html", {
                'message': 'Invalid credentials.'
            })
    return render(request, 'users/login.html')

def logout_view(request):
    logout(request)
    return render(request, "users/login.html", {
                'message': 'You are logged out.'
            })
    
def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'users/login.html')

    else:
        form = SignUpForm()

    return render(request, 'users/signup.html', {'form':form}, status=200)