# from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Hive, Membership, Task, Event
from .forms import HiveForm, TaskForm
from django.shortcuts import render, get_object_or_404, redirect

@login_required
def hive_list(request):
    # Query all hives from the database
    hives = Hive.objects.all()
    return render(request, 'hive_manager/hive_list.html', {'hives': hives})

@login_required
def hive_detail(request, hive_id):

        hive = Hive.objects.get(id=hive_id)
        memberships = Membership.objects.filter(hive=hive)
        return render(request, 'hive_manager/hive_detail.html', {'hive': hive, 'memberships': memberships})

@login_required
def create_hive(request):
    if request.method == 'POST':
        form = HiveForm(request.POST)
        if form.is_valid():
            hive = form.save(commit=False)
            hive.queen_bee = request.user
            hive.save()

            # Create membership for the Queen Bee
            Membership.objects.create(User=request.user, hive=hive, role=Membership.QueenBee)
            return redirect('hive_manager:hive_list')
    else:
        form = HiveForm()
    return render(request, 'hive_manager/create_hive.html', {'form': form})

@login_required
def update_hive(request, hive_id):
    hive = get_object_or_404(Hive, id=hive_id)
    if request.method == 'POST':
        form = HiveForm(request.POST, instance=hive)
        if form.is_valid():
            form.save()
            return redirect('hive_manager:hive_detail', hive_id=hive_id)  # Redirect to Hive detail page
    else:
        form = HiveForm(instance=hive)
    return render(request, 'hive_manager/update_hive.html', {'form': form, 'hive': hive})

@login_required
def delete_hive(request, hive_id):
    hive = get_object_or_404(Hive, id=hive_id)
    if request.method == 'POST':
        hive.delete()
        return redirect('hive_manager:hive_list')  # Redirect to Hive list page
    else:
        return render(request, 'hive_manager/delete_hive.html', {'hive': hive}) # return redirect('hive_list')


# views for creating task
def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'hive_manager/task_list.html', {'tasks': tasks})

def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    return render(request, 'hive_manager/task_detail.html', {'task': task})

def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hive_manager:task_list')
    else:
        form = TaskForm()
    return render(request, 'hive_manager/create_task.html', {'form': form})

def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('hive_manager:task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'hive_manager/update_task.html', {'form': form})

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})



@login_required
def dashboard(request):
    # Fetch data from models
    tasks = Task.objects.all()
    hives = Hive.objects.all()
    memberships = Membership.objects.all()
    events = Event.objects.all()  # Query all events from the database

    context = {
        'tasks': tasks,
        'hives': hives,
        'memberships': memberships,
        'events': events
    }
    return render(request, 'hive_manager/dashboard.html', context)

