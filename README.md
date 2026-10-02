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

1. Створіть БД `vet_crm_sandbox`
2. Скопіюйте `.env.example` → `.env.sandbox`, заповніть своїми даними
3. Запустіть:
   ```powershell
   uvicorn app.main:app --reload
   ```

### Production (робоче середовище)

1. Створіть БД `vet_crm_production`
2. Скопіюйте `.env.example` → `.env.production`, заповніть реальними production-даними (сильний `SECRET_KEY`, `DEBUG=False`)
3. Запустіть:
   ```powershell
   $env:APP_ENV="production"
   uvicorn app.main:app
   ```

За замовчуванням (`APP_ENV` не задано) застосунок працює в режимі `sandbox`.

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