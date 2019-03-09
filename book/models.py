from django.db import models


class Author(models.Model):
    name = models.CharField(primary_key=True, max_length=256, verbose_name="Author name.")

    def __str__(self):
        return self.name


# Create your models here.
class Book(models.Model):
    name = models.CharField(max_length=256, verbose_name="Book name")
    isbn = models.CharField(max_length=14, verbose_name="Book's ISBN")
    country = models.CharField(max_length=256, verbose_name="Country")
    authors = models.ManyToManyField(Author, verbose_name="Book's authors names.")
    number_of_pages = models.IntegerField(verbose_name="Number of pages in book.")
    publisher = models.CharField(max_length=256, verbose_name="Publisher of book.")
    release_date = models.CharField(max_length=256, verbose_name="Release date of book.")

    def __str__(self):
        return self.name
