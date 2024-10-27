from rest_framework import serializers

from book import models


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Book
        fields = "__all__"


class BookInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    book_marks_count = serializers.IntegerField()
    is_book_marked = serializers.BooleanField()


class CommentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = "__all__"


class BookDetailSerializer(serializers.Serializer):
    name = serializers.CharField()
    summery = serializers.CharField()
    comments_count = serializers.IntegerField()
    rates_count = serializers.IntegerField()
    rates_average = serializers.IntegerField()
    distinct_rates_count = serializers.DictField()
    comments = serializers.ListField(child=CommentModelSerializer())


class BookMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BookMark
        fields = "__all__"


class CommentRequestModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        exclude = ("user",)
