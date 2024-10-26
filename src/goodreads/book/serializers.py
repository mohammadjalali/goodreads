from rest_framework import serializers


class BookSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    book_marks_count = serializers.IntegerField()
    is_book_marked = serializers.BooleanField()


class BookDetailSerializer(serializers.Serializer):
    name = serializers.CharField()
    summery = serializers.CharField()
    comments_count = serializers.IntegerField()
    rates_count = serializers.IntegerField()
    rates_average = serializers.IntegerField()
    distinct_rates_count = serializers.DictField()
    user_comments_and_rates = serializers.ListField()
