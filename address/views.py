from django.db import IntegrityError
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from address.models import Address
from address.permissions import IsAdmin
from address.serializers import AddressSerializer
from users.models import User

# Create your views here.
class AddressView(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated, IsAdmin]

  def put(self, request):
    try:
      user = User.objects.get(uuid=request.user.uuid)
      serialized = AddressSerializer(data=request.data)

      serialized.is_valid()

      address = Address.objects.create(**serialized.validated_data)
      address.users.add(user)

      address = Address.objects.get(uuid=address.uuid)

      serialized = AddressSerializer(address)

      return Response(serialized.data, status=status.HTTP_201_CREATED)
    except IntegrityError:
      return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
    
  def get(self, request, address_id=''):
    if address_id:
      address = Address.objects.get(uuid=address_id)
      serialized = AddressSerializer(address)

      return Response(serialized.data)

    address = Address.objects.all()
    print(address[0].users)
    serialized = AddressSerializer(address, many=True)

    return Response(serialized.data)