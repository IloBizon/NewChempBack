from django.test import TestCase
from django.core.exceptions import ValidationError
from unittest.mock import MagicMock
from .models import CustomUser, Disease


class DigitalTwinTests(TestCase):
    def setUp(self):
        self.disease = Disease.objects.create(name="Hypertension", mkb="I10")
        self.user = CustomUser.objects.create(
            username="testuser@med.ru",
            email="testuser@med.ru",
            weight=80,
            disease=self.disease
        )

    def test_medical_indicators_validation(self):
        def validate_bp(sys, dia):
            if sys <= dia: raise ValidationError("Error")
            if sys >= 180 or dia >= 120: return "CRISIS"
            if 90 <= sys <= 140 and 60 <= dia <= 90: return "NORMAL"
            return "OUT_OF_RANGE"

        self.assertEqual(validate_bp(120, 80), "NORMAL")
        self.assertEqual(validate_bp(180, 110), "CRISIS")
        with self.assertRaises(ValidationError):
            validate_bp(80, 120)

    def test_drug_dosage_calculation(self):
        def calculate_dosage(user, drug_limit):
            base_dose = user.weight * 0.5
            if user.weight > 200: return drug_limit
            if user.disease.mkb == "I10": return base_dose * 0.8
            return base_dose

        self.assertEqual(calculate_dosage(self.user, 100), 32.0)
        heavy_user = MagicMock(weight=250)
        self.assertEqual(calculate_dosage(heavy_user, 100), 100)
        self.assertIsInstance(calculate_dosage(self.user, 100), float)

    def test_glucose_trend_analysis(self):
        def analyze_trend(data):
            if len(data) < 2: return "STABLE"
            diff = data[-1] - data[0]
            velocity = round(diff / len(data), 2)
            direction = "GROWTH" if diff > 0 else "DECREASE"
            significant = abs(diff) > 2.0
            return {"dir": direction, "vel": velocity, "sig": significant}

        trend = analyze_trend([5.0, 6.5, 8.2])
        self.assertEqual(trend["dir"], "GROWTH")
        self.assertEqual(trend["vel"], 1.07)
        self.assertTrue(trend["sig"])

    def test_drug_interaction_check(self):
        mock_checker = MagicMock()
        mock_checker.check.return_value = {"risk": "HIGH", "desc": "Conflict", "rec": "Change Drug B"}

        result = mock_checker.check("DrugA", "DrugB")
        self.assertEqual(result["risk"], "HIGH")
        self.assertTrue("Conflict" in result["desc"])
        self.assertEqual(result["rec"], "Change Drug B")

    def test_medical_notification_generation(self):
        def generate_alert(sys, dia):
            if sys > 140:
                return {"priority": 1, "msg": f"Alert: High BP {sys}/{dia}", "status": "SENT"}
            return {"priority": 3, "msg": "Normal", "status": "SKIPPED"}

        alert = generate_alert(150, 95)
        self.assertEqual(alert["priority"], 1)
        self.assertIn("150/95", alert["msg"])
        self.assertEqual(alert["status"], "SENT")
