
# Makefile для проекта mkapartner.ru

# Старт проекта в отсоединённом режиме
start:
	docker-compose up -d --build

# Просмотр логов сервера (как было в start)
logs:
	docker-compose logs -f

# Перезапуск без пересборки
restart:
	docker-compose restart

# Собрать статику вручную
collectstatic:
	docker-compose exec app python manage.py collectstatic --noinput

# Применить миграции
migrate:
	docker-compose exec app python manage.py migrate

# Показать маршруты
urls:
	docker-compose exec app python manage.py show_urls

# Открыть shell внутри контейнера
shell:
	docker-compose exec app sh
