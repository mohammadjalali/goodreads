from book.models.book import Book
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Comment(models.Model):

    rate = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True
    )
    comment = models.TextField(null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        self.book.name
