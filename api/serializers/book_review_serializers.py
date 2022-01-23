from rest_framework import serializers


class BookTagSerializer(serializers.Serializer):
    tag_name = serializers.CharField(max_length=20)


class BookReviewSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    title = serializers.CharField(max_length=100)
    comment = serializers.CharField()
    book_tags = BookTagSerializer(many=True)