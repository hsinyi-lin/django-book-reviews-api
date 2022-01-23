from rest_framework.response import Response


def user_login_required(function):
    def wrapper(request, *args, **kw):
        if 'user_id' not in request.session:
            return Response({'success':False, 'message': '請登入'})
        else:
            return function(request, *args, **kw)
    return wrapper