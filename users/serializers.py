from rest_framework import serializers


class UserSerializer(serializers.Serializer):
  uuid = serializers.UUIDField(format='hex_verbose', read_only=True)
  first_name = serializers.CharField()
  last_name = serializers.CharField()
  email = serializers.EmailField()
  password = serializers.CharField(write_only=True)
  is_admin = serializers.BooleanField(default=False)

class LoginSerializer(serializers.Serializer):
  email = serializers.EmailField()
  password = serializers.CharField()
