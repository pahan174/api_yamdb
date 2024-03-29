## Использованный стэк технологий
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)


# Yamdb API

REST API для сервиса YaMDb — базы отзывов о фильмах, книгах и музыке. (Совместный проект 3 студентов Яндекс.Практикум). 




## Описание

API для сервиса YaMDb. Позволяет работать со следующими сущностями:

* Отзывы (Получить список всех отзывов, создать новый отзыв, получить отзыв по id, частично обновить отзыв по id, удалить отзыв по id)

* Коментарии к отзывам (Получить список всех комментариев к отзыву по id, создать новый комментарий для отзыва, получить комментарий для отзыва по id, частично обновить комментарий к отзыву по id, удалить комментарий к отзыву по id)

* JWT-токен (Отправление confirmation_code на переданный email, получение JWT-токена в обмен на email и confirmation_code)

* Пользователи (Получить список всех пользователей, создание пользователя, получить пользователя по username, изменить данные пользователя по username, удалить пользователя по username, получить данные своей учетной записи, изменить данные своей учетной записи)

* Категории (типы) произведений (Получить список всех категорий, создать категорию, удалить категорию)

* Категории жанров (Получить список всех жанров, создать жанр, удалить жанр)

* Произведения, к которым пишут отзывы (Получить список всех объектов, создать произведение для отзывов, информация об объекте, обновить информацию об объекте, удалить произведение)

После запуска проекта, по адресу `http://127.0.0.1:8000/redoc/` будет доступна документация для Yamdb API.

## Как запустить проект:

1. Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/il-mo/api_yamdb
```

```
cd yatube_api
```

2. Cоздать и активировать виртуальное окружение:

```
python -m venv env
```

```
source env/bin/activate
```

3. Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

4. Выполнить миграции:

```
python manage.py migrate
```

5. Запустить проект:

```
python manage.py runserver
```
