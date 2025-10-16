from django.core.management.base import BaseCommand
from employees.models import Employee, Role, Department
from datetime import date
from decimal import Decimal

SAMPLES = [
    dict(first_name="Ana", last_name="Silva", email="ana.silva@empresa.com", cpf="12345678901",
         birth_date=date(1990, 5, 10), hire_date=date(2023, 2, 1),
         role=Role.DEVELOPER, department=Department.ENGINEERING,
         salary=Decimal("8500.00"), is_active=True),

    dict(first_name="Bruno", last_name="Souza", email="bruno@empresa.com", cpf="98765432100",
         birth_date=date(1988, 7, 1), hire_date=date(2020, 3, 1),
         role=Role.ANALYST, department=Department.FINANCE,
         salary=Decimal("6200.00"), is_active=True),

    dict(first_name="Carla", last_name="Mendes", email="carla.mendes@empresa.com", cpf="11122233344",
         birth_date=date(1993, 4, 20), hire_date=date(2022, 8, 15),
         role=Role.DEVELOPER, department=Department.ENGINEERING,
         salary=Decimal("7800.00"), is_active=True),

    dict(first_name="Diego", last_name="Santos", email="diego.santos@empresa.com", cpf="22233344455",
         birth_date=date(1987, 9, 12), hire_date=date(2021, 1, 10),
         role=Role.ANALYST, department=Department.ENGINEERING,
         salary=Decimal("5500.00"), is_active=True),

    dict(first_name="Eduardo", last_name="Lima", email="eduardo.lima@empresa.com", cpf="33344455566",
         birth_date=date(1985, 11, 5), hire_date=date(2019, 5, 2),
         role=Role.DEVELOPER, department=Department.OPERATIONS,
         salary=Decimal("9200.00"), is_active=True),

    dict(first_name="Fernanda", last_name="Costa", email="fernanda.costa@empresa.com", cpf="44455566677",
         birth_date=date(1991, 6, 18), hire_date=date(2021, 10, 1),
         role=Role.MANAGER, department=Department.ENGINEERING,   # PO ~ manager
         salary=Decimal("10500.00"), is_active=True),

    dict(first_name="Gabriel", last_name="Almeida", email="gabriel.almeida@empresa.com", cpf="55566677788",
         birth_date=date(1989, 2, 23), hire_date=date(2022, 4, 4),
         role=Role.ANALYST, department=Department.ENGINEERING,   # dados ~ eng
         salary=Decimal("12000.00"), is_active=True),

    dict(first_name="Heloisa", last_name="Rocha", email="heloisa.rocha@empresa.com", cpf="66677788899",
         birth_date=date(1994, 12, 3), hire_date=date(2020, 12, 15),
         role=Role.ANALYST, department=Department.MARKETING,     # UX ~ marketing
         salary=Decimal("6800.00"), is_active=True),

    dict(first_name="Igor", last_name="Pereira", email="igor.pereira@empresa.com", cpf="77788899900",
         birth_date=date(1995, 3, 8), hire_date=date(2024, 1, 20),
         role=Role.ANALYST, department=Department.SUPPORT,
         salary=Decimal("4300.00"), is_active=True),

    dict(first_name="Juliana", last_name="Ribeiro", email="juliana.ribeiro@empresa.com", cpf="88899900011",
         birth_date=date(1992, 8, 27), hire_date=date(2018, 9, 3),
         role=Role.ANALYST, department=Department.HR,
         salary=Decimal("6000.00"), is_active=True),

    dict(first_name="Kleber", last_name="Oliveira", email="kleber.oliveira@empresa.com", cpf="99900011122",
         birth_date=date(1986, 1, 30), hire_date=date(2017, 7, 7),
         role=Role.ANALYST, department=Department.FINANCE,
         salary=Decimal("8000.00"), is_active=True),
]

class Command(BaseCommand):
    help = "Cria funcionários de exemplo (11 registros)"

    def handle(self, *args, **kwargs):
        created, updated = 0, 0
        for payload in SAMPLES:
            _, was_created = Employee.objects.update_or_create(
                email=payload["email"], defaults=payload
            )
            if was_created:
                created += 1
            else:
                updated += 1
        self.stdout.write(self.style.SUCCESS(
            f"Seed ok: {len(SAMPLES)} registros (criados: {created}, atualizados: {updated})"
        ))
