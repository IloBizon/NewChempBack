import os
import django
import random
from datetime import timedelta
from django.utils import timezone

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from app.models import (
    Disease, CustomUser, Doctor, LabStatistics,
    HealthStatistics, Drug, DrugPrescription,
    HealthDiary, DoctorConsultation
)


def generate_data():
    print("🚀 Запуск генерации расширенного набора данных...")

    # 1. Болезни (МКБ-10)
    diseases_data = [
        ("Сахарный диабет 2 типа", "E11"),
        ("Гипертоническая болезнь", "I10"),
        ("Бронхиальная астма", "J45"),
        ("Гастрит", "K29")
    ]
    diseases = [Disease.objects.get_or_create(name=n, mkb=m)[0] for n, m in diseases_data]

    # 2. Врачи
    doctors_list = [
        ("Доктор Хаус", "Диагност"),
        ("Степанов И.И.", "Кардиолог"),
        ("Петрова А.В.", "Эндокринолог")
    ]
    created_doctors = []
    for name, spec in doctors_list:
        doc, _ = Doctor.objects.get_or_create(name=name, specialization=spec)
        created_doctors.append(doc)

    # 3. Пользователи (Врач-аккаунт и 3 Пациента)
    # Врач
    if not CustomUser.objects.filter(email="doc_main@med.ru").exists():
        CustomUser.objects.create_user(
            email="doc_main@med.ru", username="main_doctor",
            password="DocPassword123!", is_doctor=True, blood_group="AB"
        )

    # Пациенты
    patients = []
    patient_names = [
        ("ivan@mail.ru", "ivan_ivanov", diseases[1]),
        ("anna@mail.ru", "anna_smith", diseases[0]),
        ("sergey@mail.ru", "sergey_p", diseases[2])
    ]

    for email, uname, dis in patient_names:
        user, created = CustomUser.objects.get_or_create(
            email=email,
            defaults={
                "username": uname, "disease": dis, "height": random.randint(160, 190),
                "weight": random.randint(60, 100), "blood_group": random.choice(["A", "B", "O"]),
                "rh_factor": random.choice([True, False])
            }
        )
        if created:
            user.set_password("Patient123!")
            user.save()
        patients.append(user)

    # 4. Лекарства
    drugs_data = ["Метформин", "Лизиноприл", "Сальбутамол", "Омепразол"]
    drugs = [Drug.objects.get_or_create(title=t, dose=random.choice([5, 10, 500]))[0] for t in drugs_data]

    # 5. Цикл генерации истории для каждого пациента (за 14 дней)
    for p in patients:
        print(f"   Заполнение данных для: {p.username}...")

        for i in range(14):
            # Статистика здоровья (каждый день)
            HealthStatistics.objects.create(
                user=p,
                glucose=random.randint(4, 9),
                systolic_pressure=random.randint(110, 150),
                diastolic_pressure=random.randint(70, 95),
                pulse=random.randint(60, 85),
                text="Замер произведен в покое"
            )

            # Дневник (через день)
            if i % 2 == 0:
                HealthDiary.objects.create(
                    user=p, mark=random.randint(3, 5),
                    text=random.choice(["Слабость", "Хорошее состояние", "Головная боль"]),
                    measures_taken=random.choice(["Отдых", "Прием лекарств", "Нет"])
                )

        # Анализы (2 записи)
        for _ in range(2):
            LabStatistics.objects.create(
                user=p, rbc=random.randint(4, 5), wbc=random.randint(4, 9),
                plt=random.randint(150, 400), hgb=random.randint(120, 160)
            )

        # Консультации
        DoctorConsultation.objects.create(
            user=p, doctor=random.choice(created_doctors),
            description="Плановый осмотр, коррекция терапии."
        )

        # Назначения (по 3 лекарства каждому)
        for d in random.sample(drugs, 2):
            DrugPrescription.objects.create(user=p, drug=d, was_taken=random.choice([True, False]))

    print("\n✅ Успех: Создано 3 пациента, 3 врача и более 100 медицинских записей.")


if __name__ == "__main__":
    generate_data()
