# Backend - Funcionários (Django 5 + DRF + JWT)

## Requisitos
- Python 3.11+
- (Opcional) PostgreSQL 14+
- Pip/venv

# Variáveis de ambiente (backend/.env)
### Crie .env na raiz:
Exemplo mínimo:

### Django
- SECRET_KEY=changeme
- DEBUG=true
- ALLOWED_HOSTS=127.0.0.1,localhost
- CSRF_TRUSTED_ORIGINS=http://127.0.0.1:3000,http://localhost:3000
- CORS_ALLOWED_ORIGINS=http://127.0.0.1:3000,http://localhost:3000
- TIME_ZONE=America/Sao_Paulo


### DB / Docker (use Postgres) — se não setar, cai em SQLite
- POSTGRES_DB=app_db
- POSTGRES_USER=app
- POSTGRES_PASSWORD=app
- POSTGRES_DB=127.0.0.1
- POSTGRES_PORT=5432
- TZ=America/Sao_Paulo
- COMPOSE_PROJECT_NAME=cosmos

Se preferir SQLite em dev, deixe as variáveis de Postgres vazias e configure no settings.py para fallback.

docker-compose.yml usa variáveis de .env

# Subir Docker com o Postgres:
```bash
docker compose up -d db
```
# Comandos úteis
```bash
cd csomos-back
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

# migrações
python manage.py makemigrations
python manage.py migrate
# superuser
python manage.py createsuperuser
# (opcional) seed, para criar 11 funcionários
python manage.py seed_employees
# rodar
python manage.py runserver
```

## Auth (JWT por e‑mail)

- POST /api/auth/token/ → { email, password } ⇒ { access, refresh }

- POST /api/auth/token/refresh/ → { refresh } ⇒ { access }

Authorization: Bearer <access> em todas as rotas protegidas.

## API Funcionários

- GET /api/employees/ — lista (paginação DRF)

- POST /api/employees/ — cria

- GET /api/employees/{id}/

- PUT/PATCH /api/employees/{id}/

- DELETE /api/employees/{id}/

## Filtros suportados:

- **search**: nome completo / first / last / e‑mail (tokenizado, AND entre termos)


- **department**: value do enum (ex.: engineering, finance, ...)

Exemplos:

```bash
/api/employees/?search=ana
/api/employees/?search=ana%20sil&department=engineering
```

# Validações:

- email único, formato válido

- cpf 11 dígitos (aceita máscara; salva limpo)

- salary ≥ 0

- hire_date ≥ birth_date + 14 anos

- role/department: enum value (ex.: developer, engineering).

**Atenção à barra final:** use /api/employees/ (com /). Se quiser sem barra, configure DefaultRouter(trailing_slash=False) ou APPEND_SLASH=False

# Testes e lint

- pytest # DRF
- pytest --cov # + cobertura
- ruff check . # lint
- black --check . # format check