from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views import generic

from .models import Author, Book, Publisher, Store


class BooksView(generic.ListView):
    model = Book
    context_object_name = 'book_list'
    template_name = 'bookstore/book_temp.html'


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'bookstore/book_det_temp.html'
    b = Author.objects.all()
    queryset = Book.objects.prefetch_related('authors')

    books = []
    for book in queryset:
        authors = [a.name for a in book.authors.all()]
        books.append({'id': book.pk, 'name': book.name, 'authors': authors})

    def get_context_data(self, **kwargs):
        contex = super().get_context_data()
        contex['books'] = BookDetailView.books
        print(BookDetailView.books)
        return contex


class AuthorsView(generic.ListView):
    model = Author
    context_object_name = 'author_list'
    template_name = 'bookstore/auth_temp.html'


class AuthorDetailView(generic.DetailView):
    model = Author
    context_object_name = 'author_det'
    template_name = 'bookstore/auth_det_temp.html'


class PublisherView(generic.ListView):
    model = Publisher
    context_object_name = 'publ_list'
    template_name = 'bookstore/publ_temp.html'


class PublisherDetailView(generic.DetailView):
    model = Publisher
    context_object_name = 'publ_det'
    template_name = 'bookstore/publ_det_temp.html'


class StoreView(generic.ListView):
    model = Store
    context_object_name = 'store_list'
    template_name = 'bookstore/store_temp.html'


class StoreDetailView(generic.DetailView):
    model = Store
    context_object_name = 'store_det'
    template_name = 'bookstore/store_det_temp.html'
