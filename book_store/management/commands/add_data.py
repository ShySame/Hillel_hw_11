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
            author_li, book_li, store_li, publisher_li, ba_li, sb_li = [], [], [], [], [], []
            for i in range(number):
                author_li.append(Author(name=fake.name(),
                                        age=fake.pyint(min_value=20, max_value=88, step=1)))
                publisher_li.append(Publisher(name=fake.company()))
                book_li.append(Book(name=(fake.text(max_nb_chars=25))[:-1],
                                    pages=fake.pyint(min_value=20, max_value=666, step=1),
                                    price=fake.pydecimal(right_digits=2,
                                                         positive=True, min_value=20,
                                                         max_value=1666),
                                    rating=fake.pyfloat(right_digits=1,
                                                        positive=True, min_value=1, max_value=5),
                                    pubdate=fake.date_between(),
                                    publisher_id=random.randint(1, number)
                                    ))
                store_li.append(Store(name=fake.company()))

            for i in range(int(number * 1.5)):
                ba_li.append(BookAuthor(book_id=random.randint(1, number),
                                        author_id=random.randint(1, number)))
                sb_li.append(StoreBook(store_id=random.randint(1, number),
                                       book_id=random.randint(1, number)))

            Author.objects.bulk_create(author_li)
            Publisher.objects.bulk_create(publisher_li)
            Book.objects.bulk_create(book_li)
            Store.objects.bulk_create(store_li)
            BookAuthor.objects.bulk_create(ba_li)
            StoreBook.objects.bulk_create(sb_li)

            sys.stdout.write("!SUCCESS!")

        except (Author.DoesNotExist or Book.DoesNotExist or Publisher.DoesNotExist
                or Store.DoesNotExist or BookAuthor.DoesNotExist or StoreBook.DoesNotExist):
            raise CommandError('Smth wrong :(')
