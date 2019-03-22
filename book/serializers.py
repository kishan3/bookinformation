"""Serializer module for book models."""

from rest_framework import serializers

from book.models import Book, Author


class AuthorSerializer(serializers.ModelSerializer):
    """AuthorSerializer returning name field."""

    class Meta:
        """AuthorSerializer Meta."""

        model = Author
        fields = ('name',)


class BookSerializer(serializers.ModelSerializer):
    """BookSerializer returning all fields."""

    class Meta:
        """BookSerializer Meta."""

        model = Book
        fields = '__all__'
