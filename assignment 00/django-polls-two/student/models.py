from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["id"]
        db_table = "questions"
        verbose_name_plural = "01 Questions"

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="choices"
    )
    choice_text = models.CharField(max_length=200)
    votes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["id"]
        db_table = "choices"
        verbose_name_plural = "02 Choices"

    def __str__(self):
        return self.choice_text


class Department(models.Model):
    name = models.CharField(max_length=100)
    seat = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["id"]
        db_table = "departments"
        verbose_name_plural = "03 Departments"
        
        constraints = [
            models.CheckConstraint(
                condition=models.Q(seat__gte=0), name="only_positive"
            )
        ]
        # unique values for name that means no two departments can have 
        # the same name
        unique_together = ("name",)

    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField(default=0)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name="students"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["id"]
        db_table = "students"
        verbose_name_plural = "04 Students"
        
        # check constraint to ensure that age is greater than or equal to 0
        constraints = [
            models.CheckConstraint(
                condition=models.Q(age__gte=18), name="only_adult"
            )
        ]

    def __str__(self):
        return self.name