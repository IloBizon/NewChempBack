from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import CustomUser, HealthDiary, HealthStatistics, DoctorConsultation, DrugPrescription
from .serializers import UserRegisterSerializer, UserLoginSer, UserProfileSerializer, HealthDiarySerializer, \
    HealthStatisticsSerializer, DoctorConsultationSerializer, DrugPrescriptionSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response



class RegisterView(APIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        ser = UserRegisterSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        user = ser.save()

        token = AccessToken.for_user(user=user)
        token_refresh = RefreshToken.for_user(user=user)
        print(token)

        ser = UserRegisterSerializer(instance=user)
        return Response(
            data={
                "data": ser.data,
                "token": str(token),
                "refresh": str(token_refresh)
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
        token = AccessToken.for_user(user=user)
        token_refresh = RefreshToken.for_user(user=user)
        ser = UserRegisterSerializer(instance=user)
        return Response(
            data={
                "data": ser.data,
                "token": str(token),
                "refresh": str(token_refresh)
            }
        )


class UserDetailProfileView(APIView):
    def get(self, request, pk):
        if request.user.is_doctor:
            user = CustomUser.objects.get(id=pk)
        else:
            user = request.user

        serializer = UserProfileSerializer(instance=user)
        return Response(serializer.data)

class HealthDiaryViewSet(ModelViewSet):
    queryset = HealthDiary.objects.all()
    serializer_class = HealthDiarySerializer

    def get_queryset(self):
        return HealthDiary.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class HealthStatisticsViewSet(ModelViewSet):
    queryset = HealthStatistics.objects.all()
    serializer_class = HealthStatisticsSerializer

    def get_queryset(self):
        return HealthStatistics.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class DoctorConsultationViewSet(ModelViewSet):
    queryset = DoctorConsultation.objects.all()
    serializer_class = DoctorConsultationSerializer

    def get_queryset(self):
        return DoctorConsultation.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class DrugPrescriptionViewSet(ModelViewSet):
    queryset = DrugPrescription.objects.all()
    serializer_class = DrugPrescriptionSerializer

    def get_queryset(self):
        return DrugPrescription.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

