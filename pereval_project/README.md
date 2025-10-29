# Pereval API

## Описание задачи

Этот проект представляет собой REST API для приложения, предназначенного для сбора информации о горных перевалах, включая координаты, изображения, данные о пользователе и статус модерации. API позволяет добавлять, получать, редактировать и фильтровать данные о перевалах.

## Технологии

- Python 3.10
- Django
- Django REST Framework (DRF)
- PostgreSQL
- python-dotenv

## Установка и запуск

1.  Клонируйте репозиторий:

    ```bash
    git clone https://github.com/Mishamir29/Pereval_2.git
    cd Pereval_2/pereval_project
    ```

2.  Установите зависимости:

    ```bash
    pip install -r requirements.txt
    ```
    > Если файла `requirements.txt` нет, создайте его:
    > ```bash
    > pip freeze > requirements.txt
    > ```
    > (предварительно установив все зависимости через `pip install ...`)

3.  Настройте переменные окружения:

    Создайте файл `.env` в папке `settings/` (рядом с `settings.py`):

    ```
    FSTR_DB_HOST=localhost
    FSTR_DB_PORT=5432
    FSTR_DB_LOGIN=your_username
    FSTR_DB_PASS=your_password
    FSTR_DB_NAME=your_database_name
    ```

4.  Выполните миграции:

    ```bash
    python manage.py migrate
    ```

5.  Запустите сервер:

    ```bash
    python manage.py runserver
    ```

    API будет доступен по адресу `http://127.0.0.1:8000/api/`.

## Эндпоинты API

### 1. Добавить новый перевал (Submit Data)

- **Метод:** `POST`
- **URL:** `/api/submitData/`
- **Описание:** Принимает JSON с информацией о перевале и добавляет его в базу данных. Поле `status` автоматически устанавливается в `new`.
- **Тело запроса (пример):**

    ```json
    {
      "beauty_title": "пер. ",
      "title": "Пхия",
      "other_titles": "Триев",
      "connect": "",
      "add_time": "2021-09-22 13:18:13",
      "user": {
        "email": "qwerty@mail.ru",
        "fam": "Пупкин",
        "name": "Василий",
        "otc": "Иванович",
        "phone": "+7 555 55 55"
      },
      "coords": {
        "latitude": 45.3842,
        "longitude": 7.1525,
        "height": 1200
      },
      "level": {
        "winter": "",
        "summer": "1А",
        "autumn": "1А",
        "spring": ""
      },
      "images": [
        {
          "data": "<base64_изображения>",
          "title": "Седловина"
        }
      ]
    }
    ```

- **Ответ (успешно):**

    ```json
    {
      "status": 200,
      "message": null,
      "id": 42
    }
    ```

- **Ответ (ошибка валидации):**

    ```json
    {
      "status": 400,
      "message": "Bad Request: invalid data",
      "id": null
    }
    ```

### 2. Получить перевал по ID

- **Метод:** `GET`
- **URL:** `/api/submitData/<id>/`
- **Описание:** Возвращает полную информацию о перевале, включая `status`.
- **Ответ (успешно):**

    ```json
    {
      "id": 42,
      "beauty_title": "пер. ",
      "title": "Пхия",
      "other_titles": "Триев",
      "connect": "",
      "add_time": "2021-09-22T13:18:13Z",
      "status": "new",
      "user": {
        "email": "qwerty@mail.ru",
        "fam": "Пупкин",
        "name": "Василий",
        "otc": "Иванович",
        "phone": "+7 555 55 55"
      },
      "coords": {
        "latitude": 45.3842,
        "longitude": 7.1525,
        "height": 1200
      },
      "level": {
        "winter": "",
        "summer": "1А",
        "autumn": "1А",
        "spring": ""
      },
      "images": [
        {
          "title": "Седловина",
          "path": "uploaded_images/..."
        }
      ]
    }
    ```

- **Ответ (не найдено):**

    ```json
    {
      "message": "Pereval not found"
    }
    ```

### 3. Редактировать перевал по ID

- **Метод:** `PATCH`
- **URL:** `/api/submitData/<id>/`
- **Описание:** Обновляет информацию о перевале, **только если его статус `new`**. Редактирование полей `user` (email, fam, name, otc, phone) **запрещено**.
- **Тело запроса (пример):**

    ```json
    {
      "title": "Новое название",
      "connect": "Новое соединение"
    }
    ```

- **Ответ (успешно):**

    ```json
    {
      "state": 1,
      "message": null
    }
    ```

- **Ответ (ошибка):**

    ```json
    {
      "state": 0,
      "message": "Editing is allowed only for entries with status 'new'"
    }
    ```

### 4. Получить все перевалы пользователя по email

- **Метод:** `GET`
- **URL:** `/api/submitData/?user__email=<email>`
- **Описание:** Возвращает список всех перевалов, отправленных пользователем с указанным email.
- **Ответ (успешно):**

    ```json
    [
      {
        "id": 1,
        "title": "Пхия",
        ...
      },
      {
        "id": 2,
        "title": "Триев",
        ...
      }
    ]
    ```

## Структура базы данных

- `User`: email (unique), fam, name, otc, phone.
- `Coords`: latitude, longitude, height.
- `Pereval`: beauty_title, title, other_titles, connect, add_time, status (new/pending/accepted/rejected), связь с User и Coords, поля level (winter/summer/autumn/spring).
- `Image`: title, path.
- `PerevalImage`: связь между Pereval и Image.

## Дополнительные задания

- [x] Переменные окружения для подключения к БД.
- [x] Улучшенная структура базы данных (отделение User, Coords, Image).
- [ ] Публикация на хостинге.
- [ ] Документация через Swagger.
- [ ] Тесты.

## Автор

Михаил