from django.db import IntegrityError
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import authenticate
from rest_framework.authtoken.models import Token

from users.models import User
from users.serializers import LoginSerializer, UserSerializer

# Create your views here.
class UserView(APIView):
  def post(self, request):
    try:
      serialized = UserSerializer(data=request.data)

      serialized.is_valid()
      
      if serialized.data['is_admin']:
        user = User.objects.create_superuser(**serialized.validated_data)
      else:
        user = User.objects.create_user(**serialized.validated_data)

      serialized = UserSerializer(user)
      
      return Response(serialized.data, status=status.HTTP_201_CREATED)
    except TypeError:
      return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
    except IntegrityError:
      return Response({"message": "User already exists"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
  
  def get(self, request):
    users = User.objects.all()
    serialized = UserSerializer(users, many=True)

    return Response(serialized.data)


class LoginView(APIView):
  def post(self, request):
    try:
      serialized = LoginSerializer(data=request.data)

      serialized.is_valid()

      user = authenticate(email=serialized.data["email"], password=serialized.data["password"])
      token = Token.objects.get_or_create(user=user)[0]

      return Response({"token": token.key})
    except KeyError:
      return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
    except IntegrityError:
      return Response({"message": "wrong email/password"},status=status.HTTP_401_UNAUTHORIZED)