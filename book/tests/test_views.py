from unittest.mock import patch

import pytest
from rest_framework.test import APIRequestFactory, APIClient

from book import views
from book.tests.dummy_data import dump

pytestmark = pytest.mark.django_db


class TestExternalBookSearch:
    def test_cutomized_json_response(self):
        views.ExternalBook.customized_json_response(dump)
        assert len(dump[0]) == 7
        assert 'release_date' in dump[0]
        assert dump[0]['release_date'] == '1996-08-01'

    @patch('book.views.requests.get')
    def test_external_book_get(self, mock_get):
        mock_get.return_value.status_code = 200
        factory = APIRequestFactory()
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

    @staticmethod
    def create_book(request_factory):
        """Helper method to create book before tests."""

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
        assert resp.data['data'] == {'id': 1, 'name': 'test_from_test',
                                     'isbn': '123-456789012', 'country': 'india',
                                     'number_of_pages': 26, 'publisher': 'pub1',
                                     'release_date': '2019-05-26', 'authors': ['test1']
                                     }
        resp = views.BookViewSet.as_view({'get': 'retrieve'})(req, pk=2)
        assert resp.status_code == 404

    def test_update(self, request_factory):
        self.create_book(request_factory)
        # following is giving fields required for update so using APIClient to test patch.
        # resp = views.BookViewSet.as_view({'get': 'retrieve'})(req, pk=1)
        client = APIClient()
        resp = client.patch('/api/v1/books/1/', data={'name': 'updated_name'}, format='json')
        assert resp.status_code == 200
        assert resp.data['message'] == 'The book test_from_test was updated successfully.'
        assert resp.data['data']['name'] == 'updated_name'

    def test_delete(self, request_factory):
        self.create_book(request_factory)
        req = request_factory.delete('api/v1/books')
        resp = views.BookViewSet.as_view({'delete': 'destroy'})(req, pk=1)
        assert resp.status_code == 200
        assert resp.data['message'] == 'The book test_from_test was deleted successfully.'
        assert resp.data['data'] == []
