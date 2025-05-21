from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Book, Genre, BookGenre, UserBook
from .serializers import BookSerializer, GenreSerializer, BookGenreSerializer, UserBookSerializer
from django.conf import settings
import requests

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', None)
        if query is None:
            return Response({"error": "Query parameter 'q' is required."}, status=status.HTTP_400_BAD_REQUEST)

        url = f"http://www.aladin.co.kr/ttb/api/ItemSearch.aspx?ttbkey={settings.ALADIN_API_KEY}&Query={query}&MaxResults=10&start=1&SearchTarget=Book&output=JS&Version=20131101"
        response = requests.get(url)
        if response.status_code != 200:
            return Response({"error": "Failed to fetch data from Aladin API."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        data = response.json()
        books = []
        for item in data.get('item', []):
            book_data = {
                'title': item.get('title'),
                'author': item.get('author'),
                'publisher': item.get('publisher'),
                'isbn': item.get('isbn13'),
                'published_at': item.get('pubDate'),
                'cover_image': item.get('cover'),
                'description': item.get('description'),
            }
            books.append(book_data)

        return Response(books, status=status.HTTP_200_OK)

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

class BookGenreViewSet(viewsets.ModelViewSet):
    queryset = BookGenre.objects.all()
    serializer_class = BookGenreSerializer

class UserBookViewSet(viewsets.ModelViewSet):
    queryset = UserBook.objects.all()
    serializer_class = UserBookSerializer
