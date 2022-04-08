import csv

from django.core.management.base import BaseCommand, CommandError

from reviews.models import (Category, Comment, Genre, GenreTitle, Review,
                            Title, User)

PATH_CSV_BASE = 'static/data/'

csv_2_orm_mapping = {
    'category.csv': Category,
    'users.csv': User,
    'genre.csv': Genre,
    'titles.csv': Title,
    'genre_title.csv': GenreTitle,
    'review.csv': Review,
    'comments.csv': Comment,
}


def add_id(row, field_name):
    row[f'{field_name}_id'] = row[field_name]
    del row[field_name]


def do_import(cmd):
    for map in csv_2_orm_mapping:
        with open(f'{PATH_CSV_BASE}{map}', 'r', encoding='utf-8') as fin:
            dr = csv.DictReader(fin)
            orm_class = csv_2_orm_mapping[map]

            data = []
            for row in dr:
                if 'author' in row:
                    add_id(row, 'author')

                if 'category' in row:
                    add_id(row, 'category')

                c = orm_class(**row)
                data.append(c)

            orm_class.objects.bulk_create(data)


class Command(BaseCommand):
    help = 'Imports static CSV files into db.sqlite3'

    def handle(self, *args, **options):
        try:
            self.stdout.write(self.style.SUCCESS('CSV importing...'))
            do_import(self)
        except Exception as ex:
            raise CommandError('CSV not imported: ' + str(ex))

        self.stdout.write(self.style.SUCCESS('CSV imported!'))
