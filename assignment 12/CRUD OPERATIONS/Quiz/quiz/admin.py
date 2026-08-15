from django.contrib import admin
from quiz.models import Quiz, Question, Choice, UserScore

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(UserScore)
