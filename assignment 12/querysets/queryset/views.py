from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from queryset.forms import TeacherForm, StudentForm
from queryset.models import Student, Teacher
from django.db.models import Count, Avg, Max, Min, Sum, Q, F


class StudentRegistrationPost(View):
    def get(self, request):
        teacher_form = TeacherForm()
        student_form = StudentForm()

        # ================== Fetch Queries ==================

        # Get all students
        # students = Student.objects.all()

        # Filter by department
        # students = Student.objects.filter(department='BBA')

        # Filter by department and age
        # students = Student.objects.filter(department='BBA', age__gt=20)

        # Exclude by department
        # students = Student.objects.exclude(department='BBA')

        # Order by name ascending
        # students = Student.objects.order_by('name')
        # Order by name descending
        # students = Student.objects.order_by('-name')
        # Random order
        # students = Student.objects.order_by('?')
        # Reverse order and limit to 5
        # students = Student.objects.order_by('pk').reverse()[:5]

        # Return as dictionary
        # students = Student.objects.values()
        # Only specific fields as dictionary
        # students = Student.objects.values('name', 'department')

        # Return as tuple
        # students = Student.objects.values_list('name', 'department')
        # Return as named tuple
        # students = Student.objects.values_list('name', 'department', named=True)

        """
        Example in template using tuple:
        students = Student.objects.values_list('name', 'department')
        {% for student in students %}
            <p>{{ student.0 }} - {{ student.1 }}</p>
        {% endfor %}
        """

        # Use specific database
        # students = Student.objects.using('default')

        # Extract dates from a field
        # students = Student.objects.dates('passed_in_year', 'year', order='DESC')

        # ================== Single Object ==================
        # Get a single student by primary key or 404 if not found
        # student = get_object_or_404(Student, pk=1)

        # ================== Filtering Examples ==================
        # students = Student.objects.filter(roll__lt=10)
        # students = Student.objects.filter(roll__gt=5)
        # students = Student.objects.filter(roll__lte=10)
        # students = Student.objects.filter(roll__gte=5)
        # students = Student.objects.filter(department__exact='BBA')
        # students = Student.objects.filter(name__iexact='john')
        # students = Student.objects.filter(name__contains='John')
        # students = Student.objects.filter(name__icontains='john')
        # students = Student.objects.filter(name__startswith='J')
        # students = Student.objects.filter(name__endswith='n')
        # students = Student.objects.filter(name__regex=r'^J')
        # students = Student.objects.filter(name__iregex=r'^j')
        # students = Student.objects.filter(roll__range=(101,110))
        # students = Student.objects.filter(id__in=[1, 2, 3])  # Filter by ID

        # ================== Aggregation ==================
        # aggregate() returns summary statistics as a dictionary
        # total_students = Student.objects.aggregate(total=Count('id'))
        # total_students = Student.objects.aggregate(total=Count('id'), avg_age=Avg('age'))
        # total_students = Student.objects.aggregate(total=Count('id'), max_age=Max('age'), min_age=Min('age'))
        # total_students = Student.objects.aggregate(total=Count('id'), sum_age=Sum('age'))
        # All together
        # total_students = Student.objects.aggregate(
        #     total=Count('id'),
        #     avg_age=Avg('age'),
        #     max_age=Max('age'),
        #     min_age=Min('age'),
        #     sum_age=Sum('age')
        # )

        # ================== Annotate ==================
        # annotate() adds a calculated field to each object in a queryset
        # total_students = Student.objects.annotate(total=Count('id'))
        # total_students = Student.objects.annotate(total=Count('id'), avg_age=Avg('age'))
        # total_students = Student.objects.annotate(total=Count('id'), avg_age=Avg('age'), max_age=Max('age'), min_age=Min('age'), sum_age=Sum('age'))
        # total_students = Student.objects.annotate(total=Count('id'), avg_age=Avg('age'), max_age=Max('age'), min_age=Min('age'), sum_age=Sum('age')).filter(total__gt=1)

        # ================= Q objects =================
        # Q objects allow you to use logical operators (&, |, ~) in queries
        # students = Student.objects.filter(Q(name__startswith='J') | Q(age__gt=20))
        # students = Student.objects.filter(Q(name__startswith='J') & Q(age__gt=20))
        # students = Student.objects.filter(~Q(name__startswith='J'))

        # ================ F objects ================
        # F objects allow you to reference model fields in queries
        # total_students = Student.objects.filter(passed_out_year__gt=F('passed_in_year'))
        # total_students = Student.objects.filter(age__gt=F('marks')|)
        
        # change manager name
        students = Student.students.all()
        student = Student.students.get(id=1)
        total_students = Student.students.filter(Q(age__gt=F('marks')) | Q(marks__lt=50))
        
        
        # ================== Context ==================
        context = {
            "teacher_form": teacher_form,
            "student_form": student_form,
            "students": students,
            "student": student,
            "total_students": total_students
        }

        return render(request, "home/home.html", context)

    def post(self, request):
        teacher_form = TeacherForm(request.POST)
        student_form = StudentForm(request.POST)

        if 'teacher_submit' in request.POST:
            if teacher_form.is_valid():
                teacher_form.save()
                return redirect('StudentRegistrationPost')

        if 'student_submit' in request.POST:
            if student_form.is_valid():
                student_form.save()
                return redirect('StudentRegistrationPost')

        # ================== Context ==================
        # For POST, define same variables to avoid template errors
        students = Student.objects.filter(id__in=[1, 2, 3])
        student = get_object_or_404(Student, pk=1)
        total_students = Student.objects.annotate(total=Count('id'))

        context = {
            "teacher_form": teacher_form,
            "student_form": student_form,
            "students": students,
            "student": student,
            "total_students": total_students
        }

        return render(request, 'home/home.html', context)