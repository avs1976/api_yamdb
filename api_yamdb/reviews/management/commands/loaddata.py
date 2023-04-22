import csv
# import os
# from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import Category, Title, Genre, TitleGenre


class Command(BaseCommand):
    help = 'Load data from csv files into database'

    def handle(self, *args, **kwargs):
        # Load data into Categories
        # with open('static/data/category.csv', 'r', encoding='utf-8') as f:
        #     reader = csv.reader(f)
        #     next(reader)
        #     for row in reader:
        #         id, name, slug = row
        #         Category.objects.get_or_create(name=name, slug=slug)
        # with open('static/data/genre.csv', 'r', encoding='utf-8') as f:
        #     reader = csv.reader(f)
        #     next(reader)
        #     for row in reader:
        #         id, name, slug = row
        #         Genre.objects.get_or_create(name=name, slug=slug)
        # with open('static/data/titles.csv', 'r', encoding='utf-8') as f:
        #     reader = csv.reader(f)
        #     next(reader)
        #     for row in reader:
        #         id, name, year, category = row
        #         category = Category.objects.get(pk=category)
        #         Title.objects.get_or_create(name=name, year=year,
        #                                     category=category)
        # with open('static/data/genre_title.csv', 'r', encoding='utf-8') as f:
        #     reader = csv.reader(f)
        #     next(reader)
        #     for row in reader:
        #         id, title, genre = row
        #         title_id = Title.objects.get(pk=title)
        #         genre_id = Genre.objects.get(pk=genre)
        #         TitleGenre.objects.get_or_create(title=title_id,
        #                                          genre=genre_id)
        with open('static/data/review.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                id, title, text, author, score, pub_date = row
                # title_id = Title.objects.get(pk=title)
                # genre_id = Genre.objects.get(pk=genre)
                # TitleGenre.objects.get_or_create(title=title_id,
                #                                  genre=genre_id)
        self.stdout.write(self.style.SUCCESS('Data loaded successfully'))
