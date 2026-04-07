<div align="left">
  
# 🔄 Django Exchange Proposal App

**Приложение для обмена товарами между пользователями** — создавайте объявления, отправляйте предложения обмена, принимайте или отклоняйте их.

[![Django](https://img.shields.io/badge/Django-4.x-092e20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![SQLite](https://img.shields.io/badge/SQLite-3-003b57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Git](https://img.shields.io/badge/Git-F05032?logo=git&logoColor=white)](https://git-scm.com/)

</div>

---

## 📝 О проекте

**Django Exchange Proposal App** — это веб-приложение, позволяющее пользователям обмениваться товарами. Пользователи могут создавать объявления о товарах, предлагать обмен другим пользователям, а также принимать или отклонять входящие предложения. Проект реализован на Django с использованием SQLite в качестве базы данных.

---

## ✨ Основные возможности

- ✅ Создание, редактирование и удаление объявлений
- ✅ Отправка предложений обмена на чужие объявления
- ✅ Просмотр входящих и исходящих предложений
- ✅ Подтверждение или отклонение предложений обмена
- ✅ Личный кабинет пользователя
- ✅ Авторизация и регистрация

---

## 🛠️ Технологии

| Категория | Технологии |
|-----------|------------|
| **Язык** | Python 3.10+ |
| **Фреймворк** | Django 4.x |
| **База данных** | SQLite |
| **Контроль версий** | Git |
| **Виртуальное окружение** | venv |

---

## 📦 Требования

- Python 3.10+
- Django 4.x
- pip / venv
- SQLite
- Git

---

## 🚀 Установка и запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/dimKucher/barter
cd barter
```

### 2. Создание виртуального окружения

```bash
python -m venv venv
source venv/bin/activate  # для Linux/macOS
venv\Scripts\activate     # для Windows
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка `.env` файла

Создайте файл `.env` в корне проекта:

```env
DEBUG=True
SECRET_KEY=your_secret_key_here
ALLOWED_HOSTS=127.0.0.1,localhost
```

### 5. Применение миграций

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Создание суперпользователя

```bash
python manage.py createsuperuser
```

### 7. Сбор статики (опционально)

```bash
python manage.py collectstatic
```

### 8. Запуск сервера

```bash
python manage.py runserver
```

Сервер будет доступен по адресу: **http://127.0.0.1:8000**

---

## ✅ Запуск тестов

```bash
python manage.py test
```

---

## 🗂️ Структура проекта

```
barter/
│
├── app_ads/              # Приложение для объявлений
├── app_proposal/         # Приложение для предложений обмена
├── core/                 # Настройки проекта (settings.py)
├── templates/            # HTML-шаблоны
├── static/               # Статические файлы (CSS, JS)
├── media/                # Медиафайлы (загруженные пользователями)
├── errors/               # Кастомный обработчик ошибок
├── pagination/           # Пагинация для списков
├── manage.py
├── db.sqlite3            # База данных SQLite
├── requirements.txt
└── .env                  # Переменные окружения (не в репозитории)
```
