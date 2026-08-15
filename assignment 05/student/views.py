from django.shortcuts import render
from django.views import generic
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from student.models import Student

# Create your views here.
@method_decorator(never_cache, name='dispatch')
class StudentListView(generic.View):
    def get(self, request):
        students = Student.objects.filter(is_status=True).select_related('batch').order_by('id')
        print(list(students))
        return render(request, 'student/student-list.html', {'students': students})