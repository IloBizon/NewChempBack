from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
import string

def validate_pass(val):
    symb = list(string.punctuation)

    if not any(str(char).isdigit() for char in val) or not any((char in symb) for char in val):
        raise ValidationError("Validation password error")

def validate_height(val):
    if val > 250 or val < 100:
        raise ValidationError("Height error")

def validate_weight(val):
    if val < 30 or val > 300:
        raise ValidationError("Weight error")

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=12, validators=[validate_pass])
    login_attempts = models.SmallIntegerField(default=0)
    disease = models.CharField(max_length=123)
    height = models.IntegerField(validators=[validate_height], default=0)
    weight = models.IntegerField(validators=[validate_weight], default=0)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"


class HealthStatistics(models.Model):
    glucose = models.IntegerField()
    systolic_pressure = models.IntegerField()
    diastolic_pressure=models.IntegerField()
    pulse = models.IntegerField()
    weight = models.IntegerField()
    text = models.CharField()
    date = models.DateTimeField(auto_now_add=True)


class DrugPrescription(models.Model):
    "Назначения"
    time = models.DateTimeField(auto_now_add=True)
    drug_title = models.CharField(max_length=128)
    drug_dose = models.IntegerField()
    was_taken = models.BooleanField()

class HealthDiary(models.Model):
    "Дневник самочуствия"
    mark = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=128)
    measures_taken = models.CharField(max_length=128)
