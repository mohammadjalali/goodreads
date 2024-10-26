from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import Exists, OuterRef, Count, Avg
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from drf_spectacular.utils import extend_schema

from book import models
from book import serializers


class BookAPIView(viewsets.ViewSet):

    @extend_schema(
        responses=serializers.BookSerializer,
    )
    def list(self, request: Request) -> Response:
        """
        Return a list of all the books.
        """
        books = models.Book.objects.annotate(
            book_marks_count=Count("bookmark"),
            is_book_marked=Exists(
                models.BookMark.objects.filter(book=OuterRef("pk"), user=request.user)
            ),
        )

        serializer = serializers.BookSerializer(books, many=True)
        return Response(serializer.data)


class BookDetailAPIView(viewsets.ViewSet):
    @extend_schema(
        responses=serializers.BookDetailSerializer,
    )
    def retrieve(self, request: Request, pk: int) -> Response:
        """
        Get detail of a book
        """
        breakpoint()
        book = get_object_or_404(models.Book, pk=pk)
        comments_count = models.Comment.objects.filter(book=book).count()
        rate_data = models.Comment.objects.filter(book=book).aggregate(
            rates_count=Count("rate"), rates_average=Avg("rate")
        )
        distinct_rates_count = (
            models.Comment.objects.filter(book=book)
            .values("rate")
            .annotate(rate_count=Count("rate"))
        )
        distinct_rates_dict = {
            rate["rate"]: rate["rate_count"] for rate in distinct_rates_count
        }
        user_comments_and_rates = models.Comment.objects.filter(book=book).values(
            "user__username", "rate", "comment"
        )
        data = {
            "name": book.name,
            "summery": book.summery,
            "comments_count": comments_count,
            "rates_count": rate_data["rates_count"] or 0,
            "rates_average": rate_data["rates_average"] or 0,
            "distinct_rates_count": distinct_rates_dict,
            "user_comments_and_rates": list(user_comments_and_rates),
        }

        serializer = serializers.BookDetailSerializer(data=data)
        serializer.is_valid()
        return Response(serializer.data)
