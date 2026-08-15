from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from task.forms import TaskForm
from task.models import Task

class HomeView(View):
    def get(self, request):
        tasks = Task.objects.all()
        return render(request, 'home.html', {'tasks': tasks})

    def post(self, request):
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('HomeView')

class EditedView(View):
    def post(self, request, id):
        task = get_object_or_404(Task, id=id)
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
        return redirect('HomeView')

class IsCompleteView(View):
    def post(self, request, id):
        task = get_object_or_404(Task, id=id)
        task.is_completed = not task.is_completed
        task.save()
        return redirect('HomeView')

class DeletedView(View):
    def post(self, request, id):
        task = get_object_or_404(Task, id=id)
        task.delete()
        return redirect('HomeView')