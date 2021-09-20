all:
	@echo "make build     - Сборка Докера"
	@echo "make migrations	- Создание миграций"
	@echo "make migrate	- Применение миграций(изменение состояния БД)"
	@echo "make run	- Запуск приложения"
	@echo "make install	- Установка всех зависимостей"
	@echo "make test	- Запуск тестов"
	@echo "make coverage	- Запуск метрик тестового покрытия"

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

coverage:
	coverage run -m pytest
	coverage report -m

test:
	pytest