from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.csrf import csrf_protect
from hive_manager.models import Hive, Membership
# from django.urls import reverse_lazy

@csrf_protect
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

@csrf_protect
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')


def contact(request):
    return render(request, 'accounts/contact.html')

def home(request):
    return render(request, 'accounts/home.html')

def about(request):
    return render(request, 'accounts/about.html')


def dashboard(request):
    # Fetch data from models
    # tasks = Task.objects.all()
    hives = Hive.objects.all()
    memberships = Membership.objects.all()

    context = {
        # 'tasks': tasks,
        'hives': hives,
        'memberships': memberships,
    }
    return render(request, 'accounts/dashboard.html', context)

