
# 💼 MKA Partner — Dev README

> Проект разворачивается в Docker. Используется Django + Nginx + Gunicorn.

---

## 📦 Быстрый старт

1. **Склонируй проект**:

   ```bash
   git clone git@github.com:codarsssss/mkapartner.ru.git
   cd mkapartner.ru
   ```

2. **Создай `.env` файл**:

   ```bash
   cp .env.example .env
   ```

   🛑 **Важно!** Запроси **значения переменных из `.env`** у Арсения.

3. **Запусти проект**:

   ```bash
   docker-compose up --build
   ```

   🔄 При первом запуске автоматически выполняются:
   - `python manage.py collectstatic`
   - `python manage.py migrate`
   - запуск `gunicorn`

4. **Открой в браузере**:

   http://localhost  
   (_Порт указывать не нужно — работает через Nginx_)

---

## 🗃 База данных

📄 Файл базы данных (`db.sqlite3`) не хранится в репозитории.

🛑 **Запроси файл `db.sqlite3` у Арсения** и положи его в папку `app/`.

---

## 🖼 Media файлы

📁 Каталог `app/media/` **не содержит нужных файлов по умолчанию**.

🛑 **Обязательно запроси содержимое папки `media/` у Арсения**, иначе не будет работать загрузка изображений, партнёров, фотографий и т.д.

Папки внутри:
- `partner_photos`
- `partners`
- `practice_instance_images`
- `cache`

---

## 🛠 Работа фронтендера

> Если ты **не работаешь с Python/Django**, тебе важно знать следующее:

### 📁 Где лежат шаблоны и статика:

| Что                        | Где находится                          |
|----------------------------|----------------------------------------|
| HTML-шаблоны (Jinja-like)  | `app/homeapp/templates/`               |
| CSS / JS / изображения     | `app/homeapp/static/`                  |
| Итоговая статика (`collectstatic`) | `app/staticfiles/` (автоматически) |

### 🧪 Хочешь быстро проверить изменения?

Измени что-то в `app/homeapp/static/` или `app/homeapp/templates/` — и **обнови страницу**.  
Проект перезапускать не нужно.

> ⚠️ Если изменения не появляются, удостоверься что они попали в `staticfiles/`. Можно перезапустить контейнер:
```bash
docker-compose restart app
```

---

## 💡 Полезные команды

- Собрать статику вручную:
  ```bash
  docker-compose exec app python manage.py collectstatic --noinput
  ```

- Применить миграции:
  ```bash
  docker-compose exec app python manage.py migrate
  ```

- Проверить доступные маршруты:
  ```bash
  docker-compose exec app python manage.py show_urls
  ```

---

## 🧼 GitIgnore

В `.gitignore` уже настроено:
- Игнорируются файлы внутри `media/`, кроме `.gitkeep`
- Игнорируется результат `collectstatic` (`staticfiles/`), кроме `.gitkeep`

Это защищает репозиторий от мусора и тяжёлых файлов.


---

## 🛠 Makefile команды (для удобства фронтенда)

| Команда              | Что делает                              |
|----------------------|------------------------------------------|
| `make start`         | Запускает проект в фоне (build + up -d) |
| `make logs`          | Показывает логи приложения
| `make restart`       | Перезапускает контейнеры                 |
| `make collectstatic` | Собирает статику                         |
| `make migrate`       | Применяет миграции БД                    |
| `make urls`          | Показывает доступные URL'ы проекта       |
| `make shell`         | Заходит в bash контейнера приложения     |

