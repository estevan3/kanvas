from multiprocessing import AuthenticationError
from django.db import IntegrityError
from django.shortcuts import render
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from courses.models import Course
from courses.permissions import IsAdmin
from courses.serializers import CourseSerializer
from users.models import User

# Create your views here.
class CourseView(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAdmin]
  
  def post(self, request):
    try:
      instructor = User.objects.get(uuid=request.user.uuid)
      data = request.data
      data['created_at'] = timezone.now()
      serialized = CourseSerializer(data=data)
      
      serialized.is_valid()

      course = Course.objects.create(**serialized.validated_data)
      course.instructor = instructor

      course = Course.objects.get(uuid=course.uuid)
      serialized = CourseSerializer(course)
      
      return Response(serialized.data, status=status.HTTP_201_CREATED)
    except IntegrityError:
      return Response({'message': 'Course already exists'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

  def get(self, request, course_id=''):
    try:
      if course_id:
        course = Course.objects.get(uuid=course_id)
        serialized = CourseSerializer(course)
        return Response(serialized.data)
    except Course.DoesNotExist:
      return Response({"message": "Course does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    courses = Course.objects.all()
    serialized = CourseSerializer(courses, many=True)
    return Response(serialized.data)

  def patch(self, request, course_id=''):
    try:
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
    except Course.DoesNotExist:
      return Response({"message": "Course does not exist"}, status=status.HTTP_404_NOT_FOUND)
    except IntegrityError:
      return Response({"message": "This course name already exists"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
  
  def delete(self, request, course_id=''):
    try:
      course = Course.objects.get(uuid=course_id)
      info = course.delete()

      return Response(status=status.HTTP_204_NO_CONTENT)
    except Course.DoesNotExist:
      return Response({"message": "Course does not exist"}, status=status.HTTP_404_NOT_FOUND)

  def put(self, request, course_id):
    try:
      course = Course.objects.get(uuid=course_id)
      instructor = User.objects.get(uuid=request.data['instructor_id'])

      if not instructor.__dict__['is_admin']:
        raise AuthenticationError

      course.instructor = instructor
      course.save()

      course = Course.objects.get(uuid=course_id)
      serialized = CourseSerializer(course)

      return Response(serialized.data)
    except Course.DoesNotExist:
      return Response({"message": "Course does not exist"}, status=status.HTTP_404_NOT_FOUND)
    except User.DoesNotExist:
      return Response({"message": "Invalid instructor_id"}, status=status.HTTP_404_NOT_FOUND)
    except AuthenticationError:
      return Response({"message": "Instructor id does not belong to an admin"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class CourseStudantsView(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAdmin]

  def put(self, request, course_id):
    try:
      course = Course.objects.get(uuid=course_id)
      students_id = request.data['students_id']

      if type(students_id) != list:
        raise TypeError()
      
      students = []
      for student_id in students_id:
        students.append(User.objects.get(uuid=student_id))

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
    except User.DoesNotExist:
      return Response({"message": "Invalid students_id list"}, status=status.HTTP_404_NOT_FOUND)
    except KeyError:
      return Response({"students_id": "students_id field required"}, status=status.HTTP_400_BAD_REQUEST)
    except TypeError:
      return Response({"students_id": "expected type of students id field: list (array)"}, status=status.HTTP_400_BAD_REQUEST)