from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE


class Tutor(models.Model):
    name = models.CharField(max_length=255, null=False, default='-')
    surname = models.CharField(max_length=255, null=False, default='-')
    occupation = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    skills = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.name} {self.surname}'


class Course(models.Model):
    name = models.CharField(max_length=255, null=False, default='-')
    description = models.TextField(null=True, blank=True)
    tutors = models.ManyToManyField(Tutor, related_name='courses', blank=True)
    students = models.ManyToManyField(User, related_name='courses', blank=True)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(max_length=255, null=False, default='-')
    description = models.TextField(null=True, blank=True)
    time = models.DateTimeField()
    course = models.ForeignKey(Course, on_delete=CASCADE, related_name='lessons')

    class Meta:
        ordering = ['time']

    def __str__(self):
        return self.name
