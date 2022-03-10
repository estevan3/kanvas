from rest_framework import serializers
from users.serializers import UserSerializer


class CourseSerializer(serializers.Serializer):
  uuid = serializers.UUIDField(format='hex_verbose', read_only=True)
  name = serializers.CharField()
  demo_time = serializers.DateField()
  created_at = serializers.DateField()
  link_repo = serializers.CharField()
  
  instructor = UserSerializer(read_only=True)
  students = UserSerializer(many=True, read_only=True)