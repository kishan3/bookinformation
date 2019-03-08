# Create your views here.
import requests
from requests.exceptions import HTTPError, ConnectionError
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from book.models import Book
from book.serializers import BookSerializer

status = {
    200: "success",
    404: "not found",
    500: "internal server error"
}
FIELDS_TO_EXCLUDE = ['url', 'mediaType', 'characters', 'povCharacters']


class ExternalBook(APIView):
    @staticmethod
    def customized_json_response(list_of_data):
        for json_response in list_of_data:
            for field in FIELDS_TO_EXCLUDE:
                json_response.pop(field)
            json_response['release_date'] = json_response.pop('released')

    def get(self, request):
        book_name = request.query_params.get('name', '')
        try:
            response = requests.get("https://www.anapioficeandfire.com/api/books?name={}".format(book_name))
            response.raise_for_status()
            json_response = response.json()
        except ConnectionError:
            return Response({"error": "You are not connected to internet!"})
        except HTTPError as e:
            return Response({'status_code': e.response.status_code, 'status': status[e.response.status_code]})

        self.customized_json_response(json_response)
        return Response({'status_code': response.status_code,
                         'status': status[response.status_code],
                         'data': json_response})


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
