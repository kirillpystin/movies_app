PROJECT_NAME ?= messenger
VERSION = $(shell python3 setup.py --version | tr '+' '-')
PROJECT_NAMESPACE ?= alvassin
REGISTRY_IMAGE ?= $(PROJECT_NAMESPACE)/$(PROJECT_NAME)

all:
	@echo "make build     - Сборка Докера"
	@echo "make migrations	- Создание миграций"
	@echo "make migrate	- Применение миграций(изменение состояния БД)"
	@echo "make run	- Запуск приложения"

	@exit 0

migrations:
	 poetry run db revision --autogenerate

migrate:
	 poetry run db upgrade head

run:
	 poetry run run_server

build:
	docker-compose -f docker-compose.yaml up -d --build

install:
	pip install poetry
	poetry install
