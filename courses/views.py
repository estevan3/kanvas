from doctest import UnexpectedException
from multiprocessing import AuthenticationError
from django.shortcuts import render
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from courses.models import Course
from courses.serializers import CourseSerializer
from users.models import User
from users.serializers import UserSerializer

# Create your views here.
class CourseView(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated, IsAdminUser]
  
  def post(self, request):
    instructor = User.objects.get(uuid=request.user.uuid)
    data = request.data
    data['created_at'] = timezone.now()
    serialized = CourseSerializer(data=data)
    
    print(serialized.is_valid())

    course = Course.objects.create(**serialized.validated_data)
    course.instructor = instructor

    course = Course.objects.get(uuid=course.uuid)
    serialized = CourseSerializer(course)
    
    return Response(serialized.data, status=status.HTTP_201_CREATED)

  def get(self, request, course_id=''):
    if course_id:
      course = Course.objects.get(uuid=course_id)
      serialized = CourseSerializer(course)
      return Response(serialized.data)
    
    courses = Course.objects.all()
    serialized = CourseSerializer(courses, many=True)
    return Response(serialized.data)

  def patch(self, request, course_id=''):
    course = Course.objects.get(uuid=course_id)

    serialized = CourseSerializer(data=request.data, partial=True)
    serialized.is_valid()

    data = {**serialized.validated_data}

    for key in data.keys():
      course.__dict__[key] = data[key]
    
    course.save()

    course = Course.objects.get(uuid=course_id)
    serialized = CourseSerializer(course)

    return Response(serialized.data)
  
  def delete(self, request, course_id=''):
    try:
      course = Course.objects.get(uuid=course_id)
      info = course.delete()

      print(type(info), info)

      return Response(status=status.HTTP_204_NO_CONTENT)
    except Course.DoesNotExist:
      return Response({"message": "Course does not exist"}, status=status.HTTP_404_NOT_FOUND)

  def put(self, request, course_id):
    course = Course.objects.get(uuid=course_id)
    instructor = User.objects.get(uuid=request.data['instructor_id'])
    course.instructor = instructor
    course.save()

    course = Course.objects.get(uuid=course_id)
    serialized = CourseSerializer(course)

    return Response(serialized.data)

class CourseStudantsView(APIView):
  def put(self, request, course_id):
    try:
      course = Course.objects.get(uuid=course_id)
      students_id = request.data['students_id']
      
      students = User.objects.all()

      students = [student for student in students if str(student.__dict__['uuid']) in students_id]

      for student in students:
        if student.__dict__['is_admin']:
          raise AuthenticationError("Some student id belongs to an Instructor")
      
      course.students.set(students)
      
      course = Course.objects.get(uuid=course_id)
      serialized = CourseSerializer(course)
      
      return Response(serialized.data)
    except AuthenticationError as error:
      return Response({"message": error.args[0]}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    except Course.DoesNotExist:
      return Response({"message": "Course does not exist"}, status=status.HTTP_404_NOT_FOUND)