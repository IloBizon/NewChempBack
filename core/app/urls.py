from django.contrib import admin
from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(viewset=HealthDiaryViewSet, prefix="health-diary")
router.register(viewset=HealthStatisticsViewSet, prefix="health-statistics")
router.register(viewset=DrugPrescriptionViewSet, prefix="drug-prescription")
router.register(viewset=DoctorConsultationViewSet, prefix="consultation")
router.register(r"diseases", DiseaseViewSet, basename="diseases")

urlpatterns = [
    path("register", RegisterView.as_view()),
    path("login", LoginView.as_view()),
    path("users/", UserListView.as_view()),
    path("users/<int:pk>", UserDetailProfileView.as_view()),
    path("", include(router.urls))
]
