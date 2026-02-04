from rest_framework import serializers
from .models import CustomUser, DoctorConsultation, HealthDiary, DrugPrescription, Drug, HealthStatistics, Disease


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("email", "password", "disease", "height", "weight", "username")
        model = CustomUser
        extra_kwargs = {
            "password": {
                "write_only": True
            },
            "username": {
                "read_only": True
            },
        }
    def create(self, validated_data):
        user = CustomUser.objects.create_user(username=validated_data.get("email"), **validated_data)
        return user



class UserLoginSer(serializers.ModelSerializer):
    email = serializers.CharField(validators=[])
    class Meta:
        fields = ("email", "password")
        model = CustomUser




class DoctorConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorConsultation
        fields = "__all__"

class HealthDiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthDiary
        fields = "__all__"
        extra_kwargs = {
            "user": {
                "read_only": True
            }
        }

class DrugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drug
        fields = "__all__"
class DrugPrescriptionSerializer(serializers.ModelSerializer):
    drug = DrugSerializer()
    class Meta:
        model = DrugPrescription
        fields = "__all__"
        extra_kwargs = {
            "user": {
                "read_only": True
            }
        }

class HealthStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthStatistics
        fields = "__all__"
        extra_kwargs = {
            "user": {
                "read_only": True
            }
        }

class UserProfileSerializer(serializers.ModelSerializer):
    doctorconsultation_set = DoctorConsultationSerializer(many=True)
    healthdiary_set = HealthDiarySerializer(many=True)
    drugprescription_set = DrugPrescriptionSerializer(many=True)
    healthstatistics_set = HealthStatisticsSerializer(many=True)
    class Meta:
        model = CustomUser
        fields = (
            "email", "disease", "height", "weight", "blood_group",
            "rh_factor", "doctorconsultation_set", "healthdiary_set", "drugprescription_set", "healthstatistics_set"
        )

class DiseaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disease
        fields = "__all__"
        extra_kwargs = {
            "user": {
                "read_only": True
            }
        }