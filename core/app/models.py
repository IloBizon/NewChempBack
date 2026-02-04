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


class Disease(models.Model):
    name = models.CharField(max_length=128)
    mkb = models.CharField(max_length=128)
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128, validators=[validate_pass])
    login_attempts = models.SmallIntegerField(default=0)
    disease = models.ForeignKey(Disease, on_delete=models.SET_NULL, null=True)
    height = models.IntegerField(validators=[validate_height], default=0)
    weight = models.IntegerField(validators=[validate_weight], default=0)
    blood_group = models.CharField(max_length=2)
    rh_factor = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    last_failed_login = models.DateTimeField(null=True, blank=True)

    REQUIRED_FIELDS = ["username"]
    USERNAME_FIELD = "email"


class Doctor(models.Model):
    name = models.CharField(max_length=128)
    specialization = models.CharField(max_length=128)

class LabStatistics(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rbc = models.IntegerField()
    wbc = models.IntegerField()
    plt = models.IntegerField()
    hgb = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

class HealthStatistics(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    glucose = models.IntegerField()
    systolic_pressure = models.IntegerField()
    diastolic_pressure=models.IntegerField()
    pulse = models.IntegerField()
    text = models.CharField()
    weight = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

class Drug(models.Model):
    title = models.CharField(max_length=123)
    dose = models.IntegerField()

class DrugPrescription(models.Model):
    "Назначения"
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    drug = models.ForeignKey(Drug, on_delete=models.SET_NULL, null=True)
    was_taken = models.BooleanField()

class HealthDiary(models.Model):
    "Дневник самочуствия"
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    mark = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=128)
    measures_taken = models.CharField(max_length=128)

class DoctorConsultation(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=256)
