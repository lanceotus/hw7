from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from .models import Tutor, Course, Lesson
from django.contrib.auth.models import User


class TutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = 'id', 'name', 'surname', 'occupation', 'description', 'skills', 'courses'
    '''id = serializers.IntegerField()
    name = serializers.CharField()
    surname = serializers.CharField()
    occupation = serializers.CharField()
    description = serializers.CharField()
    skills = serializers.CharField()'''


class LessonSerializer(serializers.ModelSerializer):
    time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Lesson
        fields = 'id', 'name', 'description', 'time'


class CourseSerializer(serializers.ModelSerializer):
    permission_classes = (IsAuthenticated,)

    class Meta:
        model = Course
        fields = 'id', 'name', 'description'


class CourseDetailedSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    tutors = TutorSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = 'id', 'name', 'description', 'lessons', 'tutors'


class CourseSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'name', 'students')
        extra_kwargs = {'students': {'write_only': True}}

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if user not in instance.students.all():
            instance.students.add(user)
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'] if 'email' in validated_data else '',
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user
