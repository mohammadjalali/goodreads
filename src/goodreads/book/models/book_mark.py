from book.models.book import Book
from django.conf import settings
from django.db import models


class BookMark(models.Model):
    class Meta:
        unique_together = ("user", "book")

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
