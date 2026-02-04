from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    CustomUser, Disease, Doctor, LabStatistics,
    HealthStatistics, Drug, DrugPrescription,
    HealthDiary, DoctorConsultation
)

# Регистрация кастомного пользователя с отображением доп. полей
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'blood_group', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Medical Info', {'fields': ('disease', 'height', 'weight', 'blood_group', 'rh_factor', 'login_attempts', "is_doctor")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Medical Info', {'fields': ('email', 'disease', 'height', 'weight', 'blood_group', 'rh_factor')}),
    )

# Простая регистрация остальных моделей
@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'mkb')

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization')

@admin.register(LabStatistics)
class LabStatisticsAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'hgb')

@admin.register(HealthStatistics)
class HealthStatisticsAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'pulse')

@admin.register(Drug)
class DrugAdmin(admin.ModelAdmin):
    list_display = ('title', 'dose')

@admin.register(DrugPrescription)
class DrugPrescriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'drug', 'was_taken', 'time')

@admin.register(HealthDiary)
class HealthDiaryAdmin(admin.ModelAdmin):
    list_display = ('user', 'mark', 'date')

@admin.register(DoctorConsultation)
class DoctorConsultationAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'user', 'description')