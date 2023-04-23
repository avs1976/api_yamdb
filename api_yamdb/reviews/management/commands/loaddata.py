import csv
from django.core.management.base import BaseCommand

from reviews.models import (
    Category, Title, Genre, TitleGenre, Review, User, Comment
)


class Command(BaseCommand):
    help = 'Load data from csv files into database'

    def handle(self, *args, **kwargs):
        # Load data into Categories
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
        with open('static/data/review.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                title_name, review_text, author_username, score, pub_date = row
                try:
                    title = Title.objects.get(name=title_name)
                    author = User.objects.get(username=author_username)
                    Review.objects.get_or_create(title=title, text=review_text,
                                                 author=author, score=score,
                                                 pub_date=pub_date)
                except Exception as e:
                    print(f"Ошибка загрузки review: {e}")
        with open('static/data/comments.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                review_id, comment_text, author_username, pub_date = row
                try:
                    review = Review.objects.get(id=review_id)
                    author = User.objects.get(username=author_username)
                    Comment.objects.get_or_create(review=review,
                                                  text=comment_text,
                                                  author=author,
                                                  pub_date=pub_date)
                except Exception as e:
                    print(f"Ошибка загрузки comment: {e}")
        self.stdout.write(self.style.SUCCESS('Data loaded successfully'))
