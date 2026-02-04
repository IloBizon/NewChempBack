from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserRegisterSerializer, UserLoginSer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response



class RegisterView(APIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        ser = UserRegisterSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        user = ser.save()

        token, _ = Token.objects.get_or_create(user=user)

        ser = UserRegisterSerializer(instance=user)
        return Response(
            data={
                "data":ser.data,
                "token": token.key
            }
        )

class LoginView(APIView):
    serializer_class = UserLoginSer
    def post(self, request):
        ser = UserLoginSer(request.data)
        print(request.data)

        user = authenticate(request,email=request.data.get("email"), password=request.data.get("password"))
        if not user:
            return Response(
                data="Invalid credentials"
            )
        token, _ = Token.objects.get_or_create(user=user)
        ser = UserRegisterSerializer(instance=user)
        return Response(
            data={
                "data": ser.data,
                "token": token.key
            }
        )
