import pytest
from mixer.backend.django import mixer

pytestmark = pytest.mark.django_db


class TestAuthor:
    def test_model(self):
        authors = mixer.cycle(2).blend('book.Author', name=mixer.sequence(lambda count: "author%s" % count))
        assert len(authors) == 2
        assert authors[0].name == "author0"
        assert authors[1].name == "author1"
        assert str(authors[0]) == "author0"


class TestBook:
    def test_model(self):
        authors = mixer.cycle(2).blend('book.Author', name=mixer.sequence(lambda count: "author%s" % count))
        book = mixer.blend('book.Book', name="Test", isbn="123-456789012", country="india",
                           number_of_pages=26, publisher="pub1", release_date="2019-05-26", authors=authors)

        assert book.pk == 1
        assert book.name == "Test"
        assert book.isbn == "123-456789012"
        assert book.country == "india"
        assert book.number_of_pages == 26
        assert book.publisher == "pub1"
        assert book.release_date == "2019-05-26"
        assert book.authors.count() == 2
        assert book.authors.first().name == "author0"
        assert book.authors.last().name == "author1"
        assert str(book) == "Test"
