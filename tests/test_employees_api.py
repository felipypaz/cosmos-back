import pytest
from django.urls import reverse


# Observações:
# - A fixture auth_client autentica via JWT (por e-mail) no conftest.py
# - A fixture employee_factory cria Employee (model_bakery ou fallback)
# - role/department DEVEM usar os values do enum (TextChoices), ex.:
#   role: "developer" | "analyst" | "tech_lead" | "manager" | "intern"
#   department: "engineering" | "finance" | "hr" | "sales" | "marketing" | "operations" | "support"


@pytest.mark.django_db
def test_auth_required(api_client):
    url = reverse("employee-list")
    res = api_client.get(url)
    assert res.status_code == 401


@pytest.mark.django_db
def test_list_employees(auth_client, employee_factory):
    employee_factory(
        first_name="Ana", last_name="Silva", email="ana@empresa.com", cpf="12345678901",
        birth_date="1990-05-10", hire_date="2020-01-01",
        role="developer", department="engineering", salary="8000.00", is_active=True
    )
    employee_factory(
        first_name="Bruno", last_name="Souza", email="bruno@empresa.com", cpf="12345678902",
        birth_date="1988-03-20", hire_date="2019-06-15",
        role="analyst", department="finance", salary="6000.00", is_active=True
    )
    url = reverse("employee-list")
    res = auth_client.get(url)
    assert res.status_code == 200
    assert res.data["count"] == 2
    fields = set(res.data["results"][0].keys())
    assert {"id", "first_name", "last_name", "email", "department", "role", "salary", "is_active"} <= fields


@pytest.mark.django_db
def test_filter_by_name(auth_client, employee_factory):
    employee_factory(
        first_name="Ana", last_name="Silva", email="ana@empresa.com", cpf="12345678903",
        birth_date="1990-05-10", hire_date="2020-01-01",
        role="developer", department="engineering", salary="8000.00", is_active=True
    )
    employee_factory(
        first_name="Carla", last_name="Souza", email="carla@empresa.com", cpf="12345678904",
        birth_date="1991-07-01", hire_date="2020-01-01",
        role="analyst", department="finance", salary="6500.00", is_active=True
    )
    url = reverse("employee-list") + "?name=ana"
    res = auth_client.get(url)
    assert res.status_code == 200
    assert res.data["count"] == 1
    assert res.data["results"][0]["first_name"] == "Ana"


@pytest.mark.django_db
def test_filter_by_department_and_role(auth_client, employee_factory):
    employee_factory(
        first_name="Dev", last_name="One", email="dev1@empresa.com", cpf="12345678905",
        birth_date="1990-01-01", hire_date="2018-01-01",
        role="developer", department="engineering", salary="9000.00", is_active=True
    )
    employee_factory(
        first_name="Dev", last_name="Two", email="dev2@empresa.com", cpf="12345678906",
        birth_date="1990-01-01", hire_date="2018-01-01",
        role="developer", department="finance", salary="9000.00", is_active=True
    )
    url = reverse("employee-list") + "?department=engineering&role=developer"
    res = auth_client.get(url)
    assert res.status_code == 200
    assert res.data["count"] == 1
    item = res.data["results"][0]
    assert item["department"] == "engineering"
    assert item["role"] == "developer"


@pytest.mark.django_db
def test_create_employee_valid(auth_client):
    url = reverse("employee-list")
    payload = {
        "first_name": "Ana",
        "last_name": "Silva",
        "email": "ana.silva@empresa.com",
        "cpf": "12345678911",
        "birth_date": "1990-05-10",
        "hire_date": "2023-02-01",
        "role": "developer",
        "department": "engineering",
        "salary": "8500.00",
        "is_active": True,
    }
    res = auth_client.post(url, payload, format="json")
    assert res.status_code == 201, res.data
    assert res.data["cpf"] == "12345678911"
    assert res.data["role"] == "developer"
    assert res.data["department"] == "engineering"


@pytest.mark.django_db
def test_create_employee_invalid_age(auth_client):
    url = reverse("employee-list")
    payload = {
        "first_name": "Joao",
        "last_name": "Jr",
        "email": "jj@empresa.com",
        "cpf": "12345678912",
        "birth_date": "2015-01-01",
        "hire_date": "2025-01-01",
        "role": "analyst",
        "department": "engineering",
        "salary": "1000.00",
        "is_active": True,
    }
    res = auth_client.post(url, payload, format="json")
    assert res.status_code == 400
    assert "mínima" in str(res.data).lower() or "14" in str(res.data)


@pytest.mark.django_db
def test_update_and_delete(auth_client, employee_factory):
    emp = employee_factory(
        first_name="Temp", last_name="User", email="tmp@empresa.com", cpf="12345678913",
        birth_date="1990-01-01", hire_date="2010-01-01",
        role="intern", department="support", salary="1200.00", is_active=True
    )
    detail = reverse("employee-detail", args=[emp.id])

    res_up = auth_client.patch(detail, {"department": "finance"}, format="json")
    assert res_up.status_code == 200, res_up.data
    assert res_up.data["department"] == "finance"

    res_del = auth_client.delete(detail)
    assert res_del.status_code == 204
