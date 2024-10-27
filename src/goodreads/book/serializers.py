from book import models
from rest_framework import serializers


class BookSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    book_marks_count = serializers.IntegerField()
    is_book_marked = serializers.BooleanField()


class CommentSerializer(serializers.ModelSerializer):
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
    comments = serializers.ListField(child=CommentSerializer())
