from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'


class Quote(models.Model):
    quote = models.CharField(max_length=300)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return f'{" ".join(self.quote.split()[:3])}...'
