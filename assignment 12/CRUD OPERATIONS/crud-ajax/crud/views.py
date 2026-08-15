from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views import generic
from crud.forms import StudentForm
from crud.models import Student

# Create your views here.
class HomeView(generic.View):
    def get(self, request):
        student_qs = Student.objects.all()
        student_form = StudentForm()
        context = {
            'student_qs': student_qs,
            'student_form': student_form,
        }
        return render(request, 'home.html', context)
    
class SavedView(generic.View):
    def post(self, request):
        student_form = StudentForm(request.POST)
        if student_form.is_valid():
            sid = request.POST.get('stuid')
            name = request.POST.get('name')
            department = request.POST.get('department')
            phone = request.POST.get('phone')
            #print(sid, name, department, phone)
            if sid == '':
                studentSaved = Student(name=name, department=department, phone=phone)
            else:
                studentSaved = Student(id=sid, name=name, department=department, phone=phone)
            studentSaved.save()
            student = Student.objects.values()
            studentData = list(student)
            #print(studentData)
            return JsonResponse({'status': 1, 'studentData': studentData})
        else:
            return JsonResponse({'status': 0})
        
class DeletedView(generic.View):
    def post(self, request):
        id = request.POST.get('sid')
        if id:
            student = get_object_or_404(Student, id=id)
            student.delete()
            return JsonResponse({'status': 1})
        else:
            return JsonResponse({'status': 0})
              
class EditedView(generic.View):
    def post(self, request):
        id = request.POST.get('sid')
        # print('==========',id)
        if id:
            student = get_object_or_404(Student, id=id)
            studentData = {'id': student.id, 'name': student.name, 'department': student.department, 'phone': student.phone}
            return JsonResponse(studentData)
        else:
            return JsonResponse({'status': 0})