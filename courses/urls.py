from django.urls import path
from courses.views import CourseStudantsView, CourseView


urlpatterns = [
  path('courses/', CourseView.as_view()),
  path('courses/<str:course_id>/', CourseView.as_view()),
  path('courses/<str:course_id>/registrations/instructor/', CourseView.as_view()),
  path('courses/<str:course_id>/registrations/students/', CourseStudantsView.as_view())
]