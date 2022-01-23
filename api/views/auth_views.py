import base64

from django.db import IntegrityError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import Account
from api.serializers.auth_serializers import RegisterSerializer


@api_view(['POST'])
def register(request):
    data = request.data
    RegisterSerializer(data=data).is_valid(raise_exception=True)

    photo = request.FILES['photo']
    photo_string = str(base64.b64encode(photo.read()))[2:-1]

    try:
        Account.objects.create(id=data['id'], pwd=data['pwd'], name=data['name'],
                               gender=bool(data['gender']), photo=photo_string, birth=data['birth'])
        return Response({'success': True, 'message': '註冊成功'})
    except IntegrityError:
        return Response({'success': False, 'message': '此帳號已被註冊'}, status=status.HTTP_409_CONFLICT)


@api_view(['POST'])
def login(request):
    if 'user_id' in request.session:
        return Response({'success': False, 'message': '您已經登入'}, status=status.HTTP_403_FORBIDDEN)

    data = request.data
    try:
        user = Account.objects.get(pk=data['id'], pwd=data['pwd'])
        request.session['user_id'] = user.id
        return Response({'success': True, 'message': '登入成功'})
    except Account.DoesNotExist:
        return Response({'success': False, 'message': '帳號或密碼錯誤'}, status=status.HTTP_404_NOT_FOUND)

