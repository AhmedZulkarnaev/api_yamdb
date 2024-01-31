import csv

from django.conf import settings
from django.db import IntegrityError
from django.core.management import BaseCommand

from reviews.models import (
    CustomUser, Category, Genre, Title, GenreTitle, Review, Comment
)


MODELS = [
    CustomUser,
    Category,
    Genre,
    Title,
    GenreTitle,
    Review,
    Comment,
]
FIELDS = {
    'author': CustomUser,
    'category': Category,
    'genre': Genre,
    'title': Title,
    'review': Review,
}


def id_to_foreign_values(row):
    row_changed = row.copy()
    for key, val in zip(row.keys(), row.values()):
        if key in FIELDS.keys():
            row_changed[key] = FIELDS[key].objects.get(pk=val)
    return row_changed


def load_csv():
    for model in MODELS:
        with open(
            settings.PATH_CSV_FILES[model.__qualname__.lower()],
            encoding='utf-8',
        ) as file:
            try:
                initial = csv.DictReader(
                    file,
                    delimiter=",",
                )
                data = []
                for row in initial:
                    row = id_to_foreign_values(row)
                    data.append(model(**row))
                model.objects.bulk_create(data)
            except (ValueError, IntegrityError) as error:
                print(f'{model.__qualname__} FAIL')
                print(error)
                break
        print(f'{model.__qualname__} OK')


class Command(BaseCommand):
    def handle(self, *args, **options):
        load_csv()
