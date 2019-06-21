from django.urls import path

from educ_api import views

app_name = 'educ_api'

urlpatterns = [
    path('courses/', views.CoursesView.as_view()),
    path('courses/<int:pk>/', views.CourseView.as_view()),

    # пусть будет здесь – вдруг ещё пригодится
    # path('lessons/', views.LessonsView.as_view()),
    # path('lessons/<int:pk>/', views.LessonView.as_view()),
    # path('tutors/', views.TutorsView.as_view()),
    # path('tutors/<int:pk>/', views.TutorView.as_view()),

    path('signup/<int:pk>/', views.CourseSignupView.as_view()),
    path("auth/", views.AuthView.as_view()),
    path("users/", views.UserCreate.as_view()),
    path("mycourses/", views.MyCoursesView.as_view()),
]