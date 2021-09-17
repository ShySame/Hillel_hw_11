from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()

    def __str__(self):
        return f'{self.name}'


class Publisher(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return f'{self.name}'


class Book(models.Model):
    name = models.CharField(max_length=300)
    pages = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.FloatField()
    authors = models.ManyToManyField(Author, through='BookAuthor')
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    pubdate = models.DateField()

    def __str__(self):
        return f'{self.name}'


class BookAuthor(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        pass


class Store(models.Model):
    name = models.CharField(max_length=300)
    books = models.ManyToManyField(Book, through='StoreBook')

    def __str__(self):
        return f'{self.name}'


class StoreBook(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        pass
