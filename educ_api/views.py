from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics

from .models import Tutor, Course, Lesson
from .serializers import TutorSerializer, CourseSerializer, CourseDetailedSerializer,\
    LessonSerializer, UserSerializer, CourseSignupSerializer


class IsAdminOrAuthenticatedReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated and
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_staff
        )


class CoursesView(APIView):
    permission_classes = (IsAdminOrAuthenticatedReadOnly,)

    def get(self, request):
        items = Course.objects.all()
        serializer = CourseSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data)


class CourseView(APIView):
    permission_classes = (IsAdminOrAuthenticatedReadOnly,)

    def get(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        serializer = CourseDetailedSerializer(course)
        return Response(serializer.data)

    def delete(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        serializer = CourseDetailedSerializer(course)
        data = serializer.data
        course.delete()
        return Response(data)


class LessonsView(APIView):
    permission_classes = (IsAdminOrAuthenticatedReadOnly,)

    def get(self, request):
        items = Lesson.objects.all()
        serializer = LessonSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LessonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LessonView(APIView):
    permission_classes = (IsAdminOrAuthenticatedReadOnly,)

    def get(self, request, pk):
        lesson = get_object_or_404(Lesson, pk=pk)
        serializer = LessonSerializer(lesson)
        return Response(serializer.data)

    def delete(self, request, pk):
        lesson = get_object_or_404(Lesson, pk=pk)
        serializer = LessonSerializer(lesson)
        data = serializer.data
        lesson.delete()
        return Response(data)


class TutorsView(APIView):
    permission_classes = (IsAdminOrAuthenticatedReadOnly,)

    def get(self, request):
        items = Tutor.objects.all()
        serializer = TutorSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TutorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TutorView(APIView):
    permission_classes = (IsAdminOrAuthenticatedReadOnly,)

    def get(self, request, pk):
        tutor = get_object_or_404(Tutor, pk=pk)
        serializer = TutorSerializer(tutor)
        return Response(serializer.data)

    def delete(self, request, pk):
        tutor = get_object_or_404(Tutor, pk=pk)
        serializer = TutorSerializer(tutor)
        data = serializer.data
        tutor.delete()
        return Response(data)


class CourseSignupView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Course.objects.all()
    serializer_class = CourseSignupSerializer

    def patch(self, request, *args, **kwargs):
        request.data.clear()
        return super().patch(request, args, kwargs)

    def put(self, request, *args, **kwargs):
        return self.patch(request, args, kwargs)


class AuthView(ObtainAuthToken):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


class UserCreate(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer


class MyCoursesView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        items = Course.objects.all().filter(students__username__exact=request.user.username)
        serializer = CourseSerializer(items, many=True)
        return Response(serializer.data)
