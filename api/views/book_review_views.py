from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from api.utils.decorators import user_login_required
from api.models import Book, BookTag
from api.serializers.book_review_serializers import *


@api_view(['POST'])
@user_login_required
def add_review(request):
    data = request.data
    serializer = BookReviewSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    book_tags = serializer.validated_data['book_tags']

    user_id = request.session['user_id']
    book = Book.objects.create(user_id=user_id, name=data['name'],
                               title=data['title'], comment=data['comment'])
    # serializer.validated_data['title']

    tags = []
    for tag in book_tags:
        tag_obj = BookTag(book_no=book.pk, name=tag['tag_name'])
        tags.append(tag_obj)
    BookTag.objects.bulk_create(tags)

    tags = BookTag.objects.filter(book_no=book.pk)
    return Response({
        'success': True,
        'data': {
            'no': book.pk,
            'user_id': book.user.pk,
            'name': book.name,
            'title': book.title,
            'comment': book.comment,
            'book_tags': [
                {
                    'tag_name': tag.name
                } for tag in tags if tags.exists()
            ]
        }
    })
