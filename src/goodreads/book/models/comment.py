from book.models.book import Book
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Comment(models.Model):
    rate = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
