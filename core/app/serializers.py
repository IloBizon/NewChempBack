from rest_framework import serializers
from .models import CustomUser


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
