from book import models, serializers
from django.contrib.auth import get_user_model
from django.db.models import Avg, Count, Exists, OuterRef
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response


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
        book = get_object_or_404(models.Book, pk=pk)
        comments = models.Comment.objects.filter(book=book)
        comments_count = comments.aggregate(Count("comment"))["comment__count"]
        rates_count = comments.aggregate(Count("rate"))["rate__count"]
        rates_average = comments.aggregate(Avg("rate"))["rate__avg"]
        distinct_rates_count = dict()
        for comment in comments:
            if not comment.rate in distinct_rates_count:
                distinct_rates_count[comment.rate] = 0
            distinct_rates_count[comment.rate] += 1
        comments_data = serializers.CommentSerializer(comments, many=True).data
        data = {
            "name": book.name,
            "summery": book.summery,
            "comments_count": comments_count,
            "rates_count": rates_count,
            "rates_average": rates_average,
            "distinct_rates_count": distinct_rates_count,
            "comments": comments_data,
        }

        serializer = serializers.BookDetailSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
