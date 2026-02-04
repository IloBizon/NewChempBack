from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework import generics
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import CustomUser, HealthDiary, HealthStatistics, DoctorConsultation, DrugPrescription
from .permissions import IsDoctorOrOwner, IsDoctor
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

class BaseMedicalViewSet(ModelViewSet):
    permission_classes = [IsDoctorOrOwner]

    def get_queryset(self):
        user = self.request.user
        if user.is_doctor:
            print(123123)
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
            name = self.request.query_param.get('name')
            if name:
                queryset = queryset.filter(username__icontains=name)
            return queryset
        return CustomUser.objects.filter(id=self.request.user.id)
