import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from django.urls import reverse, NoReverseMatch

try:
    from model_bakery import baker

    HAVE_BAKERY = True
except Exception:
    HAVE_BAKERY = False


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def admin_user(db):
    return User.objects.create_user(
        username="admin",
        email="admin@empresa.com",
        password="admin",
        is_active=True,
    )


@pytest.fixture
def auth_client(api_client, admin_user):
    # suporta seu endpoint por e-mail (email_token_obtain) ou o padrão do SimpleJWT
    try:
        url = reverse("email_token_obtain")
        payload = {"email": admin_user.email, "password": "admin"}
    except NoReverseMatch:
        url = reverse("token_obtain_pair")
        payload = {"username": "admin", "password": "admin"}

    res = api_client.post(url, payload, format="json")
    assert res.status_code == 200, res.content
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {res.data['access']}")
    return api_client


@pytest.fixture
def employee_factory(db):
    def _make(**kwargs):
        if HAVE_BAKERY:
            return baker.make("employees.Employee", **kwargs)
        # fallback sem bakery
        from employees.models import Employee
        return Employee.objects.create(**kwargs)

    return _make
