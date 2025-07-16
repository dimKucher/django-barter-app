# Django Exchange Proposal App

Приложение для обмена товарами между пользователями.
Пользователи могут создавать объявления, отправлять предложения обмена и принимать или отклонять их.

## 📦 Требования

- Python 3.10+
- Django 4.x+
- pip / venv
- SQLite
- Git

## 🚀 Установка

1. **Клонируйте репозиторий:**

```bash
git clone https://github.com/dimKucher/barter
cd your-repo-name 
```

2. **Создайте виртуальное окружение:**

```bash
python -m venv venv
source venv/bin/activate  # для Linux/macOS
venv\Scripts\activate     # для Windows
```

3. **Установите зависимости:**

```bash
pip install -r requirements.txt
```

## ⚙️ Настройка проекта

1. **Создайте .env файл**

Пример .env:

```env
# .env

DEBUG=True
SECRET_KEY=your_secret_key
ALLOWED_HOSTS=127.0.0.1,localhost
```

2. **Примените миграции:**

```bash
python manage.py makemigrations
python manage.py migrate
```

3. **Создайте суперпользователя:**

```bash
python manage.py createsuperuser
```

4. **Соберите статику (если потребуется):**

```bash
python manage.py collectstatic
```

## ▶️ Запуск сервера

```bash
python manage.py runserver
```

Сервер будет доступен по адресу: http://127.0.0.1:8000

## ✅ Запуск тестов

Для запуска unit-тестов выполните:

```bash
python manage.py test
```

## 🗂️ Структура проекта (примерная)

```csharp

barter/
│
├── app_ads/              # Объявления
├── app_proposal/         # Предложения об обмене
├── core/                 # Настройки проекта
├── templates/            # HTML-шаблоны
├── static/               # Статические файлы
├───errors/               # Кастомный обработчик ошибок
├───media/                # Медиа файлы
├───pagination/           # Пагинация
├── manage.py
├── db.sqlite3             
└── requirements.txt
```

## 🧪 Поддержка и отладка

Убедитесь, что middleware MessageMiddleware включен в settings.py
Для сообщений и ошибок используйте django.contrib.messages