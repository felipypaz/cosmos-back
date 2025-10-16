import re
from datetime import date
from rest_framework import serializers
from .models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")

    def validate_cpf(self, value: str) -> str:
        digits = re.sub(r"\D", "", value or "")
        if len(digits) != 11:
            raise serializers.ValidationError("CPF deve conter 11 dígitos.")
        return digits

    def validate(self, data):
        birth = data.get("birth_date", getattr(self.instance, "birth_date", None))
        hire  = data.get("hire_date",  getattr(self.instance, "hire_date", None))
        if birth and hire:
            min_hire = date(birth.year + 14, birth.month, birth.day)
            if hire < min_hire:
                raise serializers.ValidationError({
                    "hire_date": "Contratação exige 14 anos completos após a data de nascimento."
                })
        return data

    def create(self, validated_data):
        validated_data["cpf"] = self.validate_cpf(validated_data["cpf"])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if "cpf" in validated_data:
            validated_data["cpf"] = self.validate_cpf(validated_data["cpf"])
        return super().update(instance, validated_data)
