import os
import django
import random
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from app.models import Disease, CustomUser, Doctor, HealthStatistics, Drug, DrugPrescription, HealthDiary, \
    DoctorConsultation


def run():
    print("--- ОЧИСТКА БАЗЫ ДАННЫХ ---")
    HealthStatistics.objects.all().delete()
    HealthDiary.objects.all().delete()
    DrugPrescription.objects.all().delete()
    DoctorConsultation.objects.all().delete()
    # Удаляем старых тестовых юзеров, чтобы не было конфликтов UNIQUE
    CustomUser.objects.filter(email__in=["main@mail.ru", "patient2@mail.ru", "patient3@mail.ru"]).delete()

    print("--- ГЕНЕРАЦИЯ СПРАВОЧНИКОВ ---")
    d_cardio, _ = Disease.objects.get_or_create(name="Кардиология (Гипертензия)", mkb="I10")
    d_endo, _ = Disease.objects.get_or_create(name="Эндокринология (Диабет)", mkb="E11")

    doc1, _ = Doctor.objects.get_or_create(name="Терапевт Сидоров", specialization="Общая практика")
    doc2, _ = Doctor.objects.get_or_create(name="Кардиолог Петров", specialization="Кардиология")

    drug_met, _ = Drug.objects.get_or_create(title="Метформин", dose=500)
    drug_lis, _ = Drug.objects.get_or_create(title="Лизиноприл", dose=10)
    drug_asp, _ = Drug.objects.get_or_create(title="Аспирин", dose=100)
    drugs = [drug_met, drug_lis, drug_asp]

    users_info = [
        {"email": "main@mail.ru", "disease": d_cardio, "trend": "stable"},
        {"email": "patient2@mail.ru", "disease": d_endo, "trend": "bad"},
        {"email": "patient3@mail.ru", "disease": d_cardio, "trend": "random"},
    ]

    for info in users_info:
        # Уникальный username на основе части email
        u_name = info["email"].split('@')[0]

        user = CustomUser.objects.create_user(
            email=info["email"],
            username=u_name,
            password="Qwerty123!!!",
            disease=info["disease"],
            height=random.randint(165, 185),
            weight=random.randint(70, 95),
            blood_group="O",
            rh_factor=True,
            is_doctor=False
        )

        print(f"Генерация истории для {user.email}...")

        now = timezone.now()
        # Генерируем данные за 20 дней для графиков
        for i in range(20):
            day = now - timedelta(days=i)

            # Логика трендов для графиков
            if info["trend"] == "stable":
                sys = random.randint(118, 124)
                glu = random.randint(4, 5)
            elif info["trend"] == "bad":
                sys = 120 + (20 - i)  # Рост к текущей дате
                glu = 5 + ((20 - i) / 4)
            else:
                sys = random.randint(110, 160)
                glu = random.randint(3, 10)

            stat = HealthStatistics.objects.create(
                user=user,
                glucose=int(glu),
                systolic_pressure=sys,
                diastolic_pressure=random.randint(70, 90),
                pulse=random.randint(60, 85),
                weight=user.weight + random.randint(-1, 1),
                text="Плановый замер"
            )
            # Принудительно ставим дату в прошлое (auto_now_add обходим через update)
            HealthStatistics.objects.filter(id=stat.id).update(date=day)

            # Записи в дневник каждые 2 дня
            if i % 2 == 0:
                diary = HealthDiary.objects.create(
                    user=user,
                    mark=random.randint(4, 9),
                    text=f"Симптомы: {random.choice(['слабость', 'норма', 'головная боль'])}",
                    measures_taken="Соблюдение режима"
                )
                HealthDiary.objects.filter(id=diary.id).update(date=day)

        # Назначения (по 3 на каждого)
        for d in drugs:
            # Создаем несколько записей для статистики приверженности
            for _ in range(3):
                DrugPrescription.objects.create(
                    user=user,
                    drug=d,
                    was_taken=random.choice([True, True, False])  # 66% успеха
                )

        # Консультации
        DoctorConsultation.objects.create(
            user=user,
            doctor=doc1,
            description="Рекомендована диета и регулярные замеры давления."
        )

    print("\n--- ГЕНЕРАЦИЯ ЗАВЕРШЕНА ---")
    print("Пароль для всех: Qwerty123!!!")


if __name__ == "__main__":
    run()
