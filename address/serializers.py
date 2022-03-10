from rest_framework import serializers
from users.serializers import UserSerializer


class AddressSerializer(serializers.Serializer):
  uuid = serializers.UUIDField(format='hex_verbose', read_only=True)
  street = serializers.CharField()
  house_number = serializers.IntegerField()
  city = serializers.CharField()
  state = serializers.CharField()
  zip_code = serializers.CharField()
  country = serializers.CharField()

  users = UserSerializer(many=True, read_only=True)