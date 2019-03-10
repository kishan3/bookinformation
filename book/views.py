# Create your views here.
import requests
from requests.exceptions import HTTPError, ConnectionError
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK
from rest_framework.views import APIView

from book.constants import FIELDS_TO_EXCLUDE, STATUS_CODES
from book.models import Book, Author
from book.serializers import BookSerializer


class ExternalBook(APIView):
    @staticmethod
    def customized_json_response(list_of_data):
        for json_response in list_of_data:
            for field in FIELDS_TO_EXCLUDE:
                json_response.pop(field)
            release = json_response.pop('released').split('T')[0]
            json_response['release_date'] = release

    def get(self, request):
        book_name = request.query_params.get('name', '')
        try:
            response = requests.get("https://www.anapioficeandfire.com/api/books?name={}".format(book_name))
            response.raise_for_status()
            json_response = response.json()
        except ConnectionError:
            return Response({"error": "You are not connected to internet!"})
        except HTTPError as e:
            return Response({'status_code': e.response.status_code, 'status': STATUS_CODES[e.response.status_code]})

        self.customized_json_response(json_response)
        return Response({'status_code': response.status_code,
                         'status': STATUS_CODES[response.status_code],
                         'data': json_response})


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def create(self, request, *args, **kwargs):
        author_names = request.data.get('authors', [])
        authors = []
        for author_name in author_names:
            author, _ = Author.objects.get_or_create(name=author_name)
            authors.append(author.pk)
        request.data['authors'] = authors
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = {"status_code": HTTP_201_CREATED,
                "status": STATUS_CODES[201],
                "data": [{"book": serializer.data}]
                }
        return Response(data, status=HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response(data={"status_code": response.status_code,
                              "status": STATUS_CODES[response.status_code],
                              "data": response.data},
                        status=HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        book = self.get_object()
        response = super().update(request, *args, **kwargs)
        return Response(data={"status_code": response.status_code,
                              "status": STATUS_CODES[response.status_code],
                              "message": "The book {} was updated successfully.".format(book.name),
                              "data": response.data
                              })

    def destroy(self, request, *args, **kwargs):
        book = self.get_object()
        response = super().destroy(request, *args, **kwargs)
        return Response(data={"status_code": response.status_code,
                              "status": "success",
                              "message": "The book {} was deleted successfully.".format(book.name),
                              "data": []})

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return Response(data={"status_code": response.status_code,
                              "status": STATUS_CODES[response.status_code],
                              "data": response.data})
