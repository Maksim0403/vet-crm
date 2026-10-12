# Vet CRM

CRM-система для мережі ветеринарних клінік із записом на прийом та історією хвороби пацієнтів.

## Стек

- FastAPI
- PostgreSQL + SQLAlchemy
- JWT-автентифікація, розмежування ролей (admin / user)
- ruff + pre-commit
- GitHub Actions (CI)

## Структура проєкту

```
app/
├── api/          # роутери (контролери)
├── core/         # конфігурація, безпека
├── db/           # підключення до БД, bootstrap
├── models/       # SQLAlchemy моделі
├── schemas/      # Pydantic схеми
└── services/     # бізнес-логіка
tests/            # pytest тести
docs/             # документація, схеми архітектури
deploy/           # конфігурації деплою
```

## Встановлення

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Запуск застосунку

### Sandbox (тестове середовище)

1. Створіть окрему PostgreSQL БД `vet_crm_sandbox`.
2. Скопіюйте шаблон і заповніть локальні налаштування:
   ```powershell
   Copy-Item .env.example .env.sandbox
   ```
   У `.env.sandbox` задайте `DATABASE_URL`, унікальний `SECRET_KEY`, `DEBUG=True` та `ENVIRONMENT=sandbox`.
3. Запустіть застосунок (без `APP_ENV` використовується `.env.sandbox`):
   ```powershell
   .\.venv\Scripts\uvicorn.exe app.main:app --reload
   ```

### Production (робоче середовище)

1. Створіть окрему PostgreSQL БД `vet_crm_production`. Не використовуйте sandbox database URL.
2. Створіть `.env.production` на основі шаблону та налаштуйте production credentials. Використовуйте довгий випадковий `SECRET_KEY`, `DEBUG=False` і `ENVIRONMENT=production`.
3. Запустіть:
   ```powershell
   $env:APP_ENV="production"
   .\.venv\Scripts\uvicorn.exe app.main:app
   ```

Щоб створити адміністратора, виконайте команду в тому ж середовищі, що й застосунок:

```powershell
.\.venv\Scripts\python.exe -m app.seed_admin admin@example.com "Use-a-unique-password"
```

Для production спочатку встановіть `$env:APP_ENV="production"` у цьому терміналі. Команда створить адміністратора або оновить роль і пароль користувача з таким email.

Файли `.env.sandbox` і `.env.production` містять локальні секрети, ігноруються Git та не повинні додаватися до репозиторію. `.env.example` містить лише прикладові значення.

## Swagger / API docs

Після запуску: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Тести

```powershell
pytest
```

## Якість коду

```powershell
ruff check .
ruff format .
```

Pre-commit хуки запускаються автоматично при коміті (`pre-commit install` після клонування репозиторію).