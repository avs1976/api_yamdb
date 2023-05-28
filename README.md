# YaMDb

# Описание

Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles). Произведения делятся на категории. Сами произведения в YaMDb не хранятся. В каждой категории есть произведения: книги, фильмы или музыка. Произведению может быть присвоен жанр (Genre) из списка предустановленных. Пользователи могут оставить на одно произведение один текстовый отзыв и выставить произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число).

# Технологии

**Python, Django, Django Rest, JWT**

# Установка

> ## Клонируем репозиторий
```
git clone https://github.com/avs1976/api_yamdb
cd api_yamdb
```

> ## Создаём виртуальное окружение (venv)
```
python -m venv venv
./venv/Scripts/Activate
```

> ## Загружаем все нужные библитеки
pip install -r requirements.txt

> ## Выполняем миграции и запускаем проект
```
python manage.py migrate
python manage.py runserver
```

> # Краткое описание моделей:

* **User**: модель пользователей, которая расширяет модель AbstractUser. Она имеет поля для роли, биографии, электронной почты и кода подтверждения, а также методы для определения уровней доступа.
* **Genre**: модель жанров произведений. Имеет название и слаг.
* **Category**: модель категорий (типов) произведений. Имеет название и слаг.
* **Title**: модель произведений, которые пользователи могут оценивать и комментировать. Имеет название, год выхода, описание, категорию и жанры.
* **TitleGenre**: модель, которая связывает произведение и жанр.
* **Review**: модель отзывов на произведения. Имеет заголовок, автора, текст, оценку и дату публикации.
* **Comment**: модель комментариев к отзывам. Имеет текст, автора и дату публикации.

> # Примеры использования:

## Авторизация:

**POST: /api/v1/auth/signup/**

## Действия с произведениями:

**GET: /api/v1/titles/** - все произведения

```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "name": "string",
      "year": 0,
      "rating": 0,
      "description": "string",
      "genre": [
        {
          "name": "string",
          "slug": "string"
        }
      ],
      "category": {
        "name": "string",
        "slug": "string"
      }
    }
  ]
}
```

**POST: /api/v1/titles/** - добавить произведение

```
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
```

**PATCH: /api/v1/titles/{titles_id}/** - изменить произведение

**DELETE: /api/v1/titles/{titles_id}/** - удалить произведение

## Действия с отзывами и комментариями:

**POST: /api/v1/titles/{title_id}/reviews/** - создать новый отзыв

```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```

**GET: /api/v1/titles/{title_id}/reviews/** - отзыв о произведении

```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "text": "string",
      "author": "string",
      "score": 1,
      "pub_date": "2023-08-24T14:15:22Z"
    }
  ]
}
```
**GET: /api/v1/titles/{title_id}/reviews/{review_id}/comments/** - комментариев к отзыву
```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "text": "string",
      "author": "string",
      "pub_date": "2019-08-24T14:15:22Z"
    }
  ]
}
```

**POST: /api/v1/titles/{title_id}/reviews/{review_id}/comments/** - создать новый отзыв
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```

# Авторы

* Алексей Шевцов (https://github.com/avs1976)
* Максим Матвеев (https://github.com/Impossible14)
* Яна Брылева (https://github.com/kettaryfox48)