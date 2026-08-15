from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.template.loader import render_to_string
from task.models import Task

class HomeView(View):
    def get(self, request):
        tasks = Task.objects.all().order_by('-id')
        return render(request, 'home.html', {'tasks': tasks})

    def post(self, request):
        name = request.POST.get('name')
        department = request.POST.get('department')
        phone = request.POST.get('phone')

        if name and department and phone:
            Task.objects.create(name=name, department=department, phone=phone)

        tasks = Task.objects.all().order_by('-id')
        html = render_to_string('partials/task_table.html', {'tasks': tasks}, request=request)
        return JsonResponse({'html': html})

class EditedView(View):
    def post(self, request, id):
        task = get_object_or_404(Task, id=id)
        name = request.POST.get('name')
        department = request.POST.get('department')
        phone = request.POST.get('phone')

        if name and department and phone:
            task.name = name
            task.department = department
            task.phone = phone
            task.save()

        tasks = Task.objects.all().order_by('-id')
        html = render_to_string('partials/task_table.html', {'tasks': tasks}, request=request)
        return JsonResponse({'html': html})

class IsCompleteView(View):
    def post(self, request, id):
        task = get_object_or_404(Task, id=id)
        task.is_completed = not task.is_completed
        task.save()

        tasks = Task.objects.all().order_by('-id')
        html = render_to_string('partials/task_table.html', {'tasks': tasks}, request=request)
        return JsonResponse({'html': html})

class DeletedView(View):
    def post(self, request, id):
        task = get_object_or_404(Task, id=id)
        task.delete()

        tasks = Task.objects.all().order_by('-id')
        html = render_to_string('partials/task_table.html', {'tasks': tasks}, request=request)
        return JsonResponse({'html': html})