.PHONY: help install migrate run clean setup shell admin logs

help:
	@echo "Comandos disponíveis:"
	@echo "  make setup          - Configuração inicial completa"
	@echo "  make install        - Instala dependências"
	@echo "  make migrate        - Executa migrations"
	@echo "  make run            - Inicia servidor Django"
	@echo "  make shell          - Django shell interativo"
	@echo "  make admin          - Cria superusuário"
	@echo "  make users          - Cria usuários padrão"
	@echo "  make clean          - Limpa arquivos temporários"
	@echo "  make db-up          - Inicia banco PostgreSQL"
	@echo "  make db-down        - Para banco PostgreSQL"
	@echo "  make db-logs        - Mostra logs do banco"
	@echo "  make freeze         - Atualiza requirements.txt"

setup: db-up install migrate users
	@echo "✅ Setup completo!"

install:
	pip install --upgrade pip
	pip install -r requirements.txt

migrate:
	python manage.py migrate

migrations:
	python manage.py makemigrations

run:
	python manage.py runserver

shell:
	python manage.py shell

admin:
	python manage.py createsuperuser

users:
	python manage.py create_default_users

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage

db-up:
	docker-compose up -d
	@echo "✅ PostgreSQL iniciado em localhost:5432"

db-down:
	docker-compose down

db-logs:
	docker-compose logs -f db

db-reset:
	docker-compose down -v
	docker-compose up -d
	@echo "✅ Banco resetado"

freeze:
	pip freeze > requirements.txt
	@echo "✅ requirements.txt atualizado"
