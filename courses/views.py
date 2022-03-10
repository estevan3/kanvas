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

# Create your views here.
class CourseView(APIView):
  def post(self, request):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    try:
      instructor = User.objects.get(uuid=request.user.uuid)
      request.data['created_at'] = timezone.now()
      serialized = CourseSerializer(data=request.data)

      serialized.is_valid()

      course = Course.objects.create(**serialized.validated_data)
      course.instructor = instructor

      course = Course.objects.get(uuid=course.uuid)
      serialized = CourseSerializer(course)
      
      return Response(serialized.data, status=status.HTTP_201_CREATED)
    except:
      return Response({"message": "error"}, status=status.HTTP_400_BAD_REQUEST)