import uuid
from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator, EmailValidator


class Role(models.TextChoices):
    ANALYST = "analyst", "Analista"
    DEVELOPER = "developer", "Desenvolvedor"
    TECH_LEAD = "tech_lead", "Tech Lead"
    MANAGER = "manager", "Gerente"
    INTERN = "intern", "Estagiário"


class Department(models.TextChoices):
    ENGINEERING = "engineering", "Tecnologia"
    FINANCE = "finance", "Financeiro"
    HR = "hr", "RH"
    SALES = "sales", "Vendas"
    MARKETING = "marketing", "Marketing"
    OPERATIONS = "operations", "Operações"
    SUPPORT = "support", "Suporte"


class Employee(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False,
        verbose_name="ID"
    )
    first_name = models.CharField(
        max_length=100, verbose_name="nome"
    )
    last_name = models.CharField(
        max_length=100, verbose_name="sobrenome"
    )
    email = models.EmailField(
        unique=True, validators=[EmailValidator()],
        verbose_name="e-mail",
        error_messages={"unique": "funcionário com este e-mail já existe."},
    )
    cpf = models.CharField(
        max_length=11, unique=True,
        verbose_name="CPF",
        error_messages={"unique": "funcionário com este CPF já existe."},
    )
    birth_date = models.DateField(
        verbose_name="data de nascimento"
    )
    hire_date = models.DateField(
        verbose_name="data de admissão"
    )
    department = models.CharField(
        max_length=100, choices=Department.choices,
        verbose_name="departamento"
    )
    role = models.CharField(
        max_length=100, choices=Role.choices,
        verbose_name="cargo"
    )
    salary = models.DecimalField(
        max_digits=12, decimal_places=2,
        validators=[MinValueValidator(Decimal("0"))],
        verbose_name="salário"
    )
    is_active = models.BooleanField(
        default=True, verbose_name="ativo"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="criado em"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="atualizado em"
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "funcionário"
        verbose_name_plural = "funcionários"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
