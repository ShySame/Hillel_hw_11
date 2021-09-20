import random
import sys

from book_store.models import Author, Book, BookAuthor, Publisher, Store, StoreBook

from django.core.management.base import BaseCommand, CommandError

from faker import Faker


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('number',
                            default=200,
                            type=int)

    def handle(self, *args, **kwargs):
        number = kwargs['number']
        try:
            fake = Faker()

            author_li = [Author(name=fake.name(),
                                age=fake.pyint(min_value=20, max_value=88, step=1))
                         for _ in range(1, number)]
            publisher_li = [Publisher(name=fake.company()) for _ in range(1, number)]

            Author.objects.bulk_create(author_li)
            Publisher.objects.bulk_create(publisher_li)

            book_li = [Book(name=(fake.text(max_nb_chars=25))[:-1],
                            pages=fake.pyint(min_value=20, max_value=666, step=1),
                            price=fake.pydecimal(right_digits=2,
                                                 positive=True, min_value=20,
                                                 max_value=1666),
                            rating=fake.pyfloat(right_digits=1,
                                                positive=True, min_value=1, max_value=5),
                            pubdate=fake.date_between(),
                            publisher_id=random.choice(Publisher.objects.values_list('id',
                                                                                     flat=True)))
                       for _ in range(1, number)]

            store_li = [Store(name=fake.company()) for _ in range(1, number)]

            Book.objects.bulk_create(book_li)
            Store.objects.bulk_create(store_li)

            book_list_id = Book.objects.values_list('id', flat=True)

            ba_li = [BookAuthor(book_id=random.choice(book_list_id),
                                author_id=random.choice(Author.objects.values_list('id',
                                                                                   flat=True)))
                     for _ in range(random.randint(number, number * 5))]
            sb_li = [StoreBook(store_id=random.choice(Store.objects.values_list('id', flat=True)),
                               book_id=random.choice(book_list_id))
                     for _ in range(random.randint(number, number * 5))]

            BookAuthor.objects.bulk_create(ba_li)
            StoreBook.objects.bulk_create(sb_li)

            sys.stdout.write("!SUCCESS!")

        except (Author.DoesNotExist or Book.DoesNotExist or Publisher.DoesNotExist or
                Store.DoesNotExist or BookAuthor.DoesNotExist or StoreBook.DoesNotExist):
            raise CommandError('Smth wrong :(')
