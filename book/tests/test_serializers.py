import pytest
from mixer.backend.django import mixer

from book.serializers import AuthorSerializer, BookSerializer

pytestmark = pytest.mark.django_db


class TestAuthorSerializer:
    def test_author_serializer(self):
        author = mixer.blend('book.Author', name="author")
        serializer = AuthorSerializer(author)
        assert serializer.data == {"name": "author"}


class TestBookSerializer:
    def test_book_serializer(self):
        author = mixer.blend('book.Author', name="author")
        book = mixer.blend('book.Book', name="Test", isbn="123-456789012", country="india",
                           number_of_pages=26, publisher="pub1", release_date="2019-05-26", authors=[author])
        serializer = BookSerializer(book)
        assert serializer.data == {'id': 1, 'name': 'Test', 'isbn': '123-456789012', 'country': 'india',
                                   'number_of_pages': 26, 'publisher': 'pub1', 'release_date': '2019-05-26',
                                   'authors': ['author']}
