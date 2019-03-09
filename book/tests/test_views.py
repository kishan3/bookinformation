from unittest.mock import patch

import pytest
from django.test import RequestFactory
from rest_framework.test import APIRequestFactory

from book import views

pytestmark = pytest.mark.django_db

dump = [{'url': 'https://www.anapioficeandfire.com/api/books/1', 'name': 'A Game of Thrones', 'isbn': '978-0553103540',
         'authors': ['George R. R. Martin'], 'numberOfPages': 694, 'publisher': 'Bantam Books',
         'country': 'United States', 'mediaType': 'Hardcover', 'released': '1996-08-01T00:00:00',
         'characters': ['https://www.anapioficeandfire.com/api/characters/2',
                        'https://www.anapioficeandfire.com/api/characters/12',
                        'https://www.anapioficeandfire.com/api/characters/13'],
         'povCharacters': ['https://www.anapioficeandfire.com/api/characters/148',
                           'https://www.anapioficeandfire.com/api/characters/208',
                           'https://www.anapioficeandfire.com/api/characters/232']},
        ]


class TestExternalBookSearch:
    def test_cutomized_json_response(self):
        views.ExternalBook.customized_json_response(dump)
        assert len(dump[0]) == 7
        assert 'release_date' in dump[0]
        assert dump[0]['release_date'] == '1996-08-01'

    @patch('book.views.requests.get')
    def test_external_book_get(self, mock_get):
        mock_get.return_value.status_code = 200
        factory = RequestFactory()
        req = factory.get('api/external-books')
        resp = views.ExternalBook.as_view()(req)
        assert resp.status_code == 200, 'Should return list of books.'
        assert resp.data['status'] == 'success'
        assert mock_get.called


class TestBookViewSet:
    @pytest.fixture
    def request_factory(self):
        factory = APIRequestFactory()
        return factory

    def create_book(self, request_factory):
        req = request_factory.post('api/v1/books', {
            'name': 'test_from_test',
            'isbn': '123-456789012',
            'country': 'india',
            'number_of_pages': 26,
            'authors': ['test1'],
            'publisher': 'pub1',
            'release_date': '2019-05-26'
        }, format='json')
        resp = views.BookViewSet.as_view({'post': 'create'})(req)
        return resp

    def test_create(self, request_factory):
        resp = self.create_book(request_factory)
        assert resp.status_code == 201
        assert resp.data['status'] == 'success'
        assert resp.data['data'] == [{'book': {'id': 1, 'name': 'test_from_test',
                                               'isbn': '123-456789012', 'country': 'india',
                                               'number_of_pages': 26, 'publisher': 'pub1',
                                               'release_date': '2019-05-26', 'authors': ['test1']
                                               }
                                      }]

    def test_list(self, request_factory):
        self.create_book(request_factory)
        req = request_factory.get('api/v1/books')
        resp = views.BookViewSet.as_view({'get': 'list'})(req)
        assert resp.status_code == 200
        assert resp.data['status'] == 'success'
        assert len(resp.data['data']) == 1

    def test_retrieve(self, request_factory):
        self.create_book(request_factory)
        req = request_factory.get('api/v1/books')
        resp = views.BookViewSet.as_view({'get': 'retrieve'})(req, pk=1)
        assert resp.status_code == 200
        assert resp.data['data'] == {"id": 1, "name": "test_from_test",
                                     "isbn": "123-456789012", "country": "india",
                                     "number_of_pages": 26, "publisher": "pub1",
                                     "release_date": "2019-05-26", "authors": ["test1"]
                                     }
        resp = views.BookViewSet.as_view({'get': 'retrieve'})(req, pk=2)
        assert resp.status_code == 404

    # def test_update(self, request_factory):
    #     self.create_book(request_factory)
    #     req = request_factory.patch('api/v1/books/1', {"name": "updated_name"}, format='json')
    #     resp = views.BookViewSet.as_view({'patch': 'update'})(req, pk=1)
    #     print(resp.data)
    #     assert resp.status_code == 200
    #     assert resp.data['message'] == "The book test_from_test was deleted successfully."

    def test_delete(self, request_factory):
        self.create_book(request_factory)
        req = request_factory.delete('api/v1/books')
        resp = views.BookViewSet.as_view({'delete': 'destroy'})(req, pk=1)
        assert resp.status_code == 200
        assert resp.data['message'] == "The book test_from_test was deleted successfully."
        assert resp.data['data'] == []
