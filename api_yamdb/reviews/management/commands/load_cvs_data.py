import csv

from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title, TitleGenre
from users.models import User


class Command(BaseCommand):
    help = 'Load data from csv files into database'
    map_ = {
        'static/data/users.csv': User,
        'static/data/category.csv': Category,
        'static/data/genre.csv': Genre,
        'static/data/titles.csv': Title,
        'static/data/genre_title.csv': TitleGenre,
        'static/data/review.csv': Review,
        'static/data/comments.csv': Comment,
    }
    ERROR_MESSAGE = 'Ошибка загрузки объекта модели {}: {}'

    def handle(self, *args, **kwargs):
        for path, model in self.map_.items():
            with open(path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('author'):
                        row['author_id'] = row['author']
                        del row['author']
                    if row.get('category'):
                        row['category_id'] = row['category']
                        del row['category']

                    try:
                        model.objects.get_or_create(**row)
                    except Exception as e:
                        print(self.ERROR_MESSAGE.format(model.__name__, e))

        self.stdout.write(self.style.SUCCESS('Data loaded successfully'))

