from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg, Count
from django.http import BadHeaderError, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .forms import Napomny
from .models import Author, Book, Publisher, Store
from .tasks import need_send_mail


class BooksView(generic.ListView):
    model = Book
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        q1 = Book.objects.annotate(num=Count('authors'))
        queryset = Book.objects.all().aggregate(Avg('price'))
        contex = super().get_context_data()
        contex['q'] = queryset
        contex['q1'] = q1
        return contex


class BookDetailView(generic.DetailView):
    model = Book

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
        q2 = Book.objects.select_related('publisher').get(id=self.object.id).publisher
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
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        queryset = Author.objects.all().aggregate(Avg('age'))

        contex = super().get_context_data()
        contex['q'] = queryset
        return contex


class AuthorDetailView(generic.DetailView):
    model = Author


class PublisherView(generic.ListView):
    model = Publisher
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        queryset = Author.objects.all().aggregate(Count('id'))
        pubs = Publisher.objects.annotate(num=Count('book'))
        contex = super().get_context_data()
        contex['q'] = queryset
        contex['p'] = pubs
        return contex


class PublisherDetailView(generic.DetailView):
    model = Publisher


class StoreView(generic.ListView):
    model = Store
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        queryset = Store.objects.all().aggregate(Count('id'))
        q = Store.objects.all().annotate(num=Count('books'))
        contex = super().get_context_data()
        contex['q'] = queryset
        contex['q1'] = q
        return contex


class StoreDetailView(generic.DetailView):
    model = Store

    def get_context_data(self, *args, **kwargs):
        q = Store.objects.get(id=self.object.id).books.all()
        store = []
        for i in q:
            store.append({'id': i.pk, 'books': i.name})
        contex = super().get_context_data()
        contex['store'] = store
        return contex


def napomny(request):
    if request.method == 'POST':
        form = Napomny(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            text = form.cleaned_data['text']
            date = form.cleaned_data['date']
            try:
                need_send_mail.apply_async((email, text), eta=date)

            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('bookstore:books')
    else:
        form = Napomny()

    return render(request,
                  'book_store/napomny.html',
                  {'form': form})


class AuthorCreateView(LoginRequiredMixin, CreateView):
    model = Author
    fields = ['name', 'age', ]
    login_url = '/accounts/login/'

    def get_success_url(self):
        return reverse('bookstore:author_detail', args=[self.object.id, ])


class AuthorUpdateView(LoginRequiredMixin, UpdateView):
    model = Author
    fields = ['name', 'age', ]
    login_url = '/accounts/login/'

    def get_success_url(self):
        return reverse('bookstore:author_detail', args=[self.object.id, ])


class AuthorDeleteView(LoginRequiredMixin, DeleteView):
    model = Author
    login_url = '/accounts/login/'

    def get_success_url(self):
        return reverse('bookstore:authors', args=None)
