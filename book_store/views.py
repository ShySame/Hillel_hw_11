from django.db.models import Avg, Count
from django.views import generic

from .models import Author, Book, Publisher, Store


class BooksView(generic.ListView):
    model = Book
    context_object_name = 'book_list'
    template_name = 'bookstore/book_temp.html'

    def get_context_data(self, *args, **kwargs):
        queryset = Book.objects.all().aggregate(Avg('price'))

        contex = super().get_context_data()
        contex['q'] = queryset
        return contex


class BookDetailView(generic.DetailView):
    model = Book
    context_object_name = 'book'
    template_name = 'bookstore/book_det_temp.html'
    b = Author.objects.all()

    def get_context_data(self, *args, **kwargs):
        books = []

        # --------------------------------------------------------------------------
        # Вроде как prefetch_related для оптимизации, но разницы по скорости выполнения не было,
        # так что лежи тут на память

        # queryset = Book.objects.prefetch_related('authors')
        # for book in queryset:
        #     authors = [a.name for a in book.authors.all()]
        #     books.append({'id': book.pk, 'name': book.name, 'authors': authors})

        queryset = Book.objects.get(id=self.object.id).authors.all()
        q2 = Book.objects.select_related('publisher').get(id=self.object.id)
        qaut = Book.objects.all().aggregate(Avg('price'))
        for a in queryset:
            books.append({'id': a.pk, 'authors': a.name})
        contex = super().get_context_data()
        contex['books'] = books
        contex['q2'] = q2
        contex['qaut'] = qaut
        return contex


class AuthorsView(generic.ListView):
    model = Author
    context_object_name = 'author_list'
    template_name = 'bookstore/auth_temp.html'

    def get_context_data(self, *args, **kwargs):
        queryset = Author.objects.all().aggregate(Avg('age'))

        contex = super().get_context_data()
        contex['q'] = queryset
        return contex


class AuthorDetailView(generic.DetailView):
    model = Author
    context_object_name = 'author_det'
    template_name = 'bookstore/auth_det_temp.html'


class PublisherView(generic.ListView):
    model = Publisher
    context_object_name = 'publ_list'
    template_name = 'bookstore/publ_temp.html'

    def get_context_data(self, *args, **kwargs):
        queryset = Author.objects.all().aggregate(Count('id'))

        contex = super().get_context_data()
        contex['q'] = queryset
        return contex


class PublisherDetailView(generic.DetailView):
    model = Publisher
    context_object_name = 'publ_det'
    template_name = 'bookstore/publ_det_temp.html'


class StoreView(generic.ListView):
    model = Store
    context_object_name = 'store_list'
    template_name = 'bookstore/store_temp.html'

    def get_context_data(self, *args, **kwargs):
        queryset = Store.objects.all().aggregate(Count('id'))

        contex = super().get_context_data()
        contex['q'] = queryset
        return contex


class StoreDetailView(generic.DetailView):
    model = Store
    context_object_name = 'store_det'
    template_name = 'bookstore/store_det_temp.html'
