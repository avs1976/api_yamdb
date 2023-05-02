import csv

from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title, TitleGenre
from users.models import User


class Command(BaseCommand):
    help = 'Load data from csv files into database'

    def handle(self, *args, **kwargs):
        with open('static/data/category.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                id, name, slug = row
                Category.objects.get_or_create(name=name, slug=slug)
        with open('static/data/genre.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                id, name, slug = row
                Genre.objects.get_or_create(name=name, slug=slug)
        with open('static/data/titles.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                id, name, year, category = row
                category = Category.objects.get(pk=category)
                Title.objects.get_or_create(name=name, year=year,
                                            category=category)
        with open('static/data/genre_title.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                id, title, genre = row
                title_id = Title.objects.get(pk=title)
                genre_id = Genre.objects.get(pk=genre)
                TitleGenre.objects.get_or_create(title=title_id,
                                                 genre=genre_id)
        with open('static/data/users.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                id, username, email, role, bio, first_name, last_name = row
                User.objects.get_or_create(id=id, username=username,
                                           email=email,
                                           role=role, bio=bio,
                                           first_name=first_name,
                                           last_name=last_name)
        with open('static/data/review.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                if len(row) != 6:
                    print("Ошибка: неправильный формат данных")
                    continue
                id, title_id, text, author_id, score, pub_date = row
                if any(char in title_id
                       + text + author_id + score
                       + pub_date for char in ['\n', '\r', '\t']):
                    print(f'Ошибка: специальные символы в данных - {row}')
                    continue
                try:
                    title_obj = Title.objects.get(id=title_id)
                except Title.DoesNotExist:
                    print(f"Ошибка: Title с именем {name} не найден")
                    continue
                try:
                    author_obj = User.objects.get(id=author_id)
                except User.DoesNotExist:
                    print(f"Ошибка: User с именем {username} не найден")
                    continue
                Review.objects.get_or_create(title=title_obj, text=text,
                                             author=author_obj, score=score,
                                             pub_date=pub_date)
        with open('static/data/comments.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                id, review_id, text, author_id, pub_date = row
                try:
                    review = Review.objects.get(id=review_id)
                    author = User.objects.get(id=author_id)
                    Comment.objects.get_or_create(review=review,
                                                  text=text,
                                                  author=author,
                                                  pub_date=pub_date)
                except Exception as e:
                    print(f"Ошибка загрузки comment: {e}")

        self.stdout.write(self.style.SUCCESS('Data loaded successfully'))
