from rest_framework import serializers
from .models import Book, Genre, BookGenre, UserBook

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'publisher', 'isbn', 'published_at', 'cover_image', 'description']

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name', 'color']

class BookGenreSerializer(serializers.ModelSerializer):
    book = BookSerializer()
    genre = GenreSerializer()

    class Meta:
        model = BookGenre
        fields = ['id', 'book', 'genre']

class UserBookSerializer(serializers.ModelSerializer):
    book = BookSerializer()

    class Meta:
        model = UserBook
        fields = ['id', 'user', 'book', 'status', 'finished_at', 'personal_note']
