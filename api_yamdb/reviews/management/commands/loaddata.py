import csv
import os
from django.conf import settings
from django.core.management.base import BaseCommand

# from reviews.models import Category


class Command(BaseCommand):
    help = 'Load data from csv files into database'

    def handle(self, *args, **okwargs):
        # Load data into Categories
        with open('static/data/category.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                id, name, slug = row
                # Category.objects.get_or_create(name=name, slug=slug)
                print(row)

            self.stdout.write(self.style.SUCCESS('Data loaded successfully'))