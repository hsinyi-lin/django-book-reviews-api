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


@api_view(['PUT'])
@user_login_required
def edit_review(request, pk):
    book_no = pk
    user_id = request.session['user_id']
    user_book = Book.objects.filter(no=book_no, user_id=user_id)
    if not user_book.exists():
        return Response({'result': False, 'message': '沒有此書'}, status=status.HTTP_404_NOT_FOUND)

    data = request.data
    serializer = BookReviewSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    user_book.update(name=data['name'], title=data['title'], comment=data['comment'])

    tags = BookTag.objects.filter(book_no=book_no)
    tags.delete()

    new_tags = []
    book_tags = serializer.validated_data['book_tags']

    for tag in book_tags:
        tag_obj = BookTag(book_no=book_no, name=tag['tag_name'])
        new_tags.append(tag_obj)
    BookTag.objects.bulk_create(new_tags)

    book = get_object_or_404(Book, pk=book_no)
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


@api_view()
@user_login_required
def get_all_reviews(request):
    user_id = request.session['user_id']

    books = Book.objects.filter(user_id=user_id)
    return Response({
        'success': True,
        'data': [
            {
                'no': book.no,
                'user_id': book.user.pk,
                'name': book.name,
                'title': book.title,
                'comment': book.comment,
                'book_tags': [
                    {
                        "tag_name": tag.name
                    }
                    for tag in BookTag.objects.filter(book_no=book.pk)
                ]
            }
            for book in books
        ]
    })


@api_view(['DELETE'])
@user_login_required
def delete_review(request, pk):
    book_no = pk
    user_id = request.session['user_id']
    book = Book.objects.filter(no=book_no, user_id=user_id)
    if not book.exists():
        return Response({'success': False, 'message': '沒有此評論'}, status=status.HTTP_404_NOT_FOUND)

    book_tags = BookTag.objects.filter(book_no=book_no)
    book_tags.delete()
    book.delete()

    return Response({'success': True, 'message': '刪除成功'})


