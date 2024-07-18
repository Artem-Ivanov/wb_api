# wb_adapter_view



## Разработка

- Склонировать проект
```bash
git clone git@git.1cupis.org:ng/python-services/wb-adapter-view.git
```
- Установить зависимости с помощью `poetry` 1.6.1.
```bash
cd wb-adapter-view/src/backend
poetry install
```

- Установить pre-commit хуки для линтинга и форматирования кода:
```bash
pre-commit install --hook-type pre-commit
```

- Поднять инфраструктурные сервисы
```bash
docker compose up
```

- Активировать виртуальное окружение (либо использовать poetry для запуска команд, указанных ниже)
```bash
source .venv/bin/activate
```

## Входные точки

### Django server

```bash
python manage.py runserver
```

```bash
make django
```

### Kafka worker

```bash
python manage.py run_kafka_worker
```

```bash
make kafka
```

### Celery worker

```bash
celery -A settings worker -Q DEFAULT_QUEUE
```

```bash
make celery
```

### Celery beat

```bash
celery -A settings beat
```

```bash
make beat
```

### Celery worker и beat в одном процессе

```bash
celery -A settings worker --beat --loglevel=debug -Q DEFAULT_QUEUE
```

### Celery worker и beat в одном процессе (с метриками)

```bash
cd src/backend && mkdir ./prometheus_metrics &&
PROMETHEUS_MULTIPROC_DIR=./prometheus_metrics celery -A settings worker --beat -Q DEFAULT_QUEUE
```

### Запуск всего проекта в сборе в профиле приложения

Эта команда позволяет запустить все необходимые процессы для работы проекта в docker compose,
в т.ч. эмуляторы. Эта команда будет наиболее интересна тестировщикам проекта.

```bash
docker compose --profile app up
```

## Первый деплой проекта

Краткий чеклист перед первым запуском проекта на prod:

- Проверить значения в конфигмапе на актуальность и заполненность
- Проверить, что все секреты используют Vault
  - [Практическая документация](https://wiki.1cupis.org/pages/viewpage.action?pageId=252847469)
  - [Структура секретов](https://wiki.1cupis.org/pages/viewpage.action?pageId=255925342)
- Проверить наличие всех необходимых деплойментов, в т.ч. ServiceAccount
- Проверить, что сервис может быть подключен к Keycloak, и все пользователи имеют необходимые роли

Полный и более актуальный чеклист деплоя находится тут: https://wiki.1cupis.org/pages/viewpage.action?pageId=282886106