from django.contrib import admin

from .models import Course, Lesson, Tutor


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    pass


@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    pass
