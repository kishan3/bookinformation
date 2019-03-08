from django.urls import path, include
from rest_framework.routers import DefaultRouter

from book.views import ExternalBook, BookViewSet

books_router = DefaultRouter()
books_router.register(r'api/v1/books', BookViewSet, basename='book')

urlpatterns = [
    path(r'', include(books_router.urls)),
    path(r'api/external-books', ExternalBook.as_view(), name="external-books"),

]
