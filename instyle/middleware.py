from django.http import HttpResponseRedirect
from signup.models import Token
import re


def simple_middleware(get_response):
    def middleware(request):
        url = request.path
        url_post = r'/post/[A-Za-z0-9]{12}'
        if url == '/login/' or url == '/signup/' or\
              url == '/login/login/' or url == '/signup/create/' or\
                url == '/login/confirm/' or url == '/login/yandex/' or\
                url == '/login/change-forgot-password-page/' or url == '/login/change-password/' or\
                url == '/login/login-forgot-password/' or url == '/login/login-change-password/':
            return get_response(request)
        if request.method == 'GET' and re.match(url_post, url):
            return get_response(request)
        
            
        token = request.COOKIES.get('instyle_token')
        try:
            Token.objects.get(token=token)
        except Token.DoesNotExist:
            return HttpResponseRedirect('/login/')

        return get_response(request)
    return middleware