
# Makefile для проекта mkapartner.ru

# Старт проекта в отсоединённом режиме
start:
	docker-compose up -d --build

# Остановить и удалить все контейнеры
stop:
	docker-compose down

# Просмотр логов сервера (как было в start)
logs:
	docker-compose logs -f

# Перезапуск без пересборки
restart:
	docker-compose restart

# Собрать статику вручную
collectstatic:
	docker-compose exec app python manage.py collectstatic --noinput

# Создать миграции
migrations:
	docker-compose exec app python manage.py makemigrations

# Применить миграции
migrate:
	docker-compose exec app python manage.py migrate

# Показать маршруты
urls:
	docker-compose exec app python manage.py show_urls

# Открыть shell внутри контейнера
shell:
	docker-compose exec app sh

# Полная очистка Docker: образы, кэш, volume'ы
clean:
	docker image prune -a -f
	docker builder prune -f
	docker system prune -a --volumes -f

# Создать суперпользователя root/root
createsuperuser:
	docker-compose exec app sh -c "echo \"from django.contrib.auth import get_user_model; \
	User = get_user_model(); \
	User.objects.filter(username='root').exists() or \
	User.objects.create_superuser('root', 'root@example.com', 'root')\" | python manage.py shell"

# Dev: старт проекта с dev-настройками
start-dev:
	docker-compose -f docker-compose.yaml -f docker-compose.dev.yaml up -d --build

# Остановить dev-сборку
stop-dev:
	docker-compose -f docker-compose.yaml -f docker-compose.dev.yaml down

logs-dev:
	docker-compose -f docker-compose.yaml -f docker-compose.dev.yaml logs -f

restart-dev:
	docker-compose -f docker-compose.yaml -f docker-compose.dev.yaml restart

collectstatic-dev:
	docker-compose -f docker-compose.yaml -f docker-compose.dev.yaml exec app python manage.py collectstatic --noinput

migrations-dev:
	docker-compose -f docker-compose.yaml -f docker-compose.dev.yaml exec app python manage.py makemigrations

migrate-dev:
	docker-compose -f docker-compose.yaml -f docker-compose.dev.yaml exec app python manage.py migrate

urls-dev:
	docker-compose -f docker-compose.yaml -f docker-compose.dev.yaml exec app python manage.py show_urls

shell-dev:
	docker-compose -f docker-compose.yaml -f docker-compose.dev.yaml exec app sh
