import csv
import os

from django.core.management.base import BaseCommand
from django.conf import settings
from reviews.models import Category, Genre, Title, GenreTitle


class Command(BaseCommand):
    help = 'Импорт данных из CSV файлов'

    def handle(self, *args, **kwargs):
        try:
            self.import_categories()
            self.import_genres()
            self.import_titles()
            self.import_genre_title()
            self.stdout.write(
                self.style.SUCCESS('Данные успешно импортированы')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Ошибка при импорте данных: {e}')
            )

    def import_categories(self):
        path = os.path.join(settings.BASE_DIR, 'static/data/category.csv')
        try:
            with open(path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                Category.objects.bulk_create(
                    Category(**row) for row in reader
                )
                self.stdout.write(
                    self.style.SUCCESS('Категории успешно импортированы')
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Ошибка при импорте категорий: {e}')
            )
            raise e

    def import_genres(self):
        path = os.path.join(settings.BASE_DIR, 'static/data/genre.csv')
        try:
            with open(path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                Genre.objects.bulk_create(
                    Genre(**row) for row in reader
                )
                self.stdout.write(
                    self.style.SUCCESS('Жанры успешно импортированы')
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Ошибка при импорте жанров: {e}')
            )
            raise e

    def import_titles(self):
        path = os.path.join(settings.BASE_DIR, 'static/data/titles.csv')
        try:
            with open(path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                titles = []
                for row in reader:
                    category_id = row.pop('category')
                    titles.append(
                        Title(
                            **row,
                            category_id=category_id
                        )
                    )
                Title.objects.bulk_create(titles)
                self.stdout.write(
                    self.style.SUCCESS('Произведения успешно импортированы')
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Ошибка при импорте произведений: {e}')
            )
            raise e

    def import_genre_title(self):
        path = os.path.join(settings.BASE_DIR, 'static/data/genre_title.csv')
        try:
            with open(path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                genre_titles = []
                for row in reader:
                    genre_titles.append(
                        GenreTitle(
                            genre_id=row['genre_id'],
                            title_id=row['title_id']
                        )
                    )
                GenreTitle.objects.bulk_create(genre_titles)
                self.stdout.write(
                    self.style.SUCCESS(
                        'Связи жанров и произведений успешно импортированы'
                    )
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f'Ошибка при импорте связей жанров и произведений: {e}'
                )
            )
            raise e
