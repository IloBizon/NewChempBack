from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .models import CustomUser, HealthDiary, HealthStatistics, DoctorConsultation, DrugPrescription, Disease
from .permissions import IsDoctorOrOwner, IsDoctor
from .serializers import UserRegisterSerializer, UserLoginSer, UserProfileSerializer, HealthDiarySerializer, \
    HealthStatisticsSerializer, DoctorConsultationSerializer, DrugPrescriptionSerializer, DiseaseSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import timedelta
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from .serializers import UserLoginSer, UserRegisterSerializer
from .models import CustomUser



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
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response(
                {"detail": "Пользователь с таким email не найден"},
                status=404
            )

        BLOCK_TIME = 1
        MAX_ATTEMPTS = 2

        if user.login_attempts >= MAX_ATTEMPTS:
            if user.last_failed_login:
                unlock_time = user.last_failed_login + timedelta(minutes=BLOCK_TIME)
                now = timezone.now()

                if now < unlock_time:
                    remaining_time = int((unlock_time - now).total_seconds() // 60)
                    return Response(
                        {"detail": f"Аккаунт заблокирован. Попробуйте через {remaining_time + 1} мин."},
                        status=403
                    )
                else:
                    user.login_attempts = 0
                    user.save()

        authenticated_user = authenticate(request, email=email, password=password)

        if authenticated_user:
            user.login_attempts = 0
            user.last_failed_login = None
            user.save()

            token = AccessToken.for_user(user=user)
            token_refresh = RefreshToken.for_user(user=user)

            user_data = UserRegisterSerializer(instance=user).data

            return Response({
                "data": user_data,
                "token": str(token),
                "refresh": str(token_refresh)
            }, status=200)

        else:
            user.login_attempts += 1
            user.last_failed_login = timezone.now()
            user.save()

            attempts_left = MAX_ATTEMPTS - user.login_attempts

            if attempts_left > 0:
                msg = f"Неверный пароль. Осталась {attempts_left} попытка."
            else:
                msg = f"Аккаунт заблокирован на {BLOCK_TIME} минут."

            return Response(
                {"detail": msg},
                status=401
            )

class UserDetailProfileView(APIView):
    def get(self, request, pk):
        if request.user.is_doctor:
            user = CustomUser.objects.get(id=pk)
        else:
            user = request.user

        serializer = UserProfileSerializer(instance=user)
        return Response(serializer.data)

class BaseMedicalViewSet(ModelViewSet):
    permission_classes = [IsDoctorOrOwner]

    def get_queryset(self):
        user = self.request.user
        if user.is_doctor:
            patient_id = self.request.query_params.get('patient_id')
            if patient_id:
                return self.queryset.filter(user_id=patient_id)
            return self.queryset.all()
        return self.queryset.filter(user=user)

    def perform_create(self, serializer):
        if self.request.user.is_doctor:
            serializer.save()
        else:
            serializer.save(user=self.request.user)

class HealthDiaryViewSet(BaseMedicalViewSet):
    queryset = HealthDiary.objects.all()
    serializer_class = HealthDiarySerializer

class HealthStatisticsViewSet(BaseMedicalViewSet):
    queryset = HealthStatistics.objects.all()
    serializer_class = HealthStatisticsSerializer

class DrugPrescriptionViewSet(BaseMedicalViewSet):
    queryset = DrugPrescription.objects.all()
    serializer_class = DrugPrescriptionSerializer

class DoctorConsultationViewSet(BaseMedicalViewSet):
    queryset = DoctorConsultation.objects.all()
    serializer_class = DoctorConsultationSerializer


class UserListView(generics.ListAPIView):
    permission_classes = [IsDoctor]
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        if self.request.user.is_doctor:
            queryset = CustomUser.objects.filter(is_doctor=False)
            name = self.request.query_params.get('name')
            if name:
                queryset = queryset.filter(username__icontains=name)
            return queryset
        return CustomUser.objects.filter(id=self.request.user.id)


class DiseaseViewSet(ReadOnlyModelViewSet):
    queryset = Disease.objects.all()
    serializer_class = DiseaseSerializer
    permission_class = [AllowAny]