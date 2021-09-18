from django.urls import path

from . import views

app_name = 'bookstore'
urlpatterns = [
    path('books/', views.BooksView.as_view(), name='books'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),

    path('author/', views.AuthorsView.as_view(), name='authors'),
    path('author/<int:pk>/', views.AuthorDetailView.as_view(), name='author_detail'),

    path('publisher/', views.PublisherView.as_view(), name='publisher'),
    path('publisher/<int:pk>/', views.PublisherDetailView.as_view(), name='publisher_detail'),

    path('store/', views.StoreView.as_view(), name='store'),
    path('store/<int:pk>/', views.StoreDetailView.as_view(), name='store_detail'),

    path('napomny/', views.napomny, name='namopny')

]
