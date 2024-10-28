from copy import copy
from typing import Mapping

from book import models, serializers
from django.db.models import Avg, Count, Exists, OuterRef, QuerySet, Value
from django.db.models.functions import Coalesce
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import authentication, permissions, status, views, viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from user.models import User


class BookAPIView(viewsets.ViewSet):
    authentication_classes = [authentication.TokenAuthentication]

    @extend_schema(
        responses=serializers.BookInfoSerializer,
    )
    def list(self, request: Request) -> Response:
        """
        Return a list of all the books.
        """
        books = models.Book.objects.annotate(
            book_marks_count=Count("bookmark"),
            is_book_marked=Coalesce(
                (
                    Exists(
                        models.BookMark.objects.filter(
                            book=OuterRef("pk"), user=request.user
                        )
                    )
                    if request.user.is_authenticated
                    else Value(False)
                ),
                Value(False),
            ),
        )

        serializer = serializers.BookInfoSerializer(books, many=True)
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
        distinct_rates_count = self._get_distinct_rates_count(comments)
        comments_data = serializers.CommentModelSerializer(comments, many=True).data
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
        return Response(serializer.data, status=status.HTTP_200_OK)

    def _get_distinct_rates_count(
        self, comments: QuerySet[models.Comment]
    ) -> Mapping[int, int]:
        distinct_rates_count = dict()
        for comment in comments:
            if not comment.rate in distinct_rates_count:
                distinct_rates_count[comment.rate] = 0
            distinct_rates_count[comment.rate] += 1
        return distinct_rates_count


class BookMarkAPIView(views.APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(responses=serializers.BookMarkSerializer)
    def post(self, request: Request, book_pk: int) -> Response:
        """
        Api to bookmark a book.
        """
        user = request.user
        book = get_object_or_404(models.Book, pk=book_pk)
        if models.Comment.objects.filter(user=user, book=book):
            return Response(
                {"message": "User is already has a comment or rate on the book."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            bookmark = models.BookMark.objects.create(user=user, book=book)
        except IntegrityError:
            return Response(
                {"message": "Book is already bookmarked."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            serializers.BookMarkSerializer(instance=bookmark).data,
            status=status.HTTP_200_OK,
        )

    @extend_schema()
    def delete(self, request: Request, book_pk: int) -> Response:
        """
        Api to delete a bookmark.
        """
        user = request.user
        book = get_object_or_404(models.Book, pk=book_pk)
        bookmark = get_object_or_404(models.BookMark, user=user, book=book)
        bookmark.delete()
        return Response(
            {"message": "Book is deleted successfully."}, status=status.HTTP_200_OK
        )


class BookMarkAPIViewset(viewsets.ViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request: Request) -> Response:
        """
        List of books user bookmarked.
        """
        user = request.user
        books = [
            bookmarks.book for bookmarks in models.BookMark.objects.filter(user=user)
        ]
        serializer_data = serializers.BookSerializer(books, many=True).data
        return Response(serializer_data, status=status.HTTP_200_OK)


class CommentAPIView(views.APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._status_code = status.HTTP_201_CREATED

    @extend_schema(
        request=serializers.CommentRequestModelSerializer,
        responses=serializers.CommentModelSerializer,
    )
    def post(self, request: Request) -> Response:
        request_serializer = serializers.CommentRequestModelSerializer(
            data=request.data
        )
        request_serializer.is_valid(raise_exception=True)
        comment_serializer = self._get_comment_serializer(
            request_serializer.validated_data, request.user
        )

        self._update_or_create_comment(request.user, comment_serializer)

        self._delete_bookmark_if_available(
            request.user, comment_serializer.validated_data["book"]
        )

        return Response(comment_serializer.data, status=self._status_code)

    def _get_comment_serializer(
        self, request_validated_data, user: User
    ) -> serializers.CommentModelSerializer:
        validated_data = copy(request_validated_data)
        validated_data["user"] = user.pk
        if "book" in validated_data:
            validated_data["book"] = request_validated_data["book"].id
        comment_serializer = serializers.CommentModelSerializer(data=validated_data)
        comment_serializer.is_valid(raise_exception=True)
        return comment_serializer

    def _update_or_create_comment(
        self, user: User, comment_serializer: serializers.CommentModelSerializer
    ) -> None:
        comment = models.Comment.objects.filter(
            user=user, book=comment_serializer.validated_data["book"]
        ).first()
        if comment:
            comment_serializer.update(
                instance=comment, validated_data=comment_serializer.validated_data
            )
            self._status_code = status.HTTP_200_OK
        else:
            comment_serializer.create(comment_serializer.validated_data)

    def _delete_bookmark_if_available(self, user: User, book: models.Book) -> None:
        bookmark = models.BookMark.objects.filter(user=user, book=book).first()
        if bookmark:
            bookmark.delete()
