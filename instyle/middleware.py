from django.http import HttpResponseRedirect
from signup.models import Token


def simple_middleware(get_response):
    def middleware(request):
        url = request.path
        response = get_response(request)
        
        if url == '/login/' or url == '/signup/' or url == '/login/login/':
            return response
            
        token = request.COOKIES.get('instyle_token')
        token_model = {}
        try:
            token_model = Token.objects.get(token=token)
        except Token.DoesNotExist:
            response = HttpResponseRedirect('/login/')
    
        return response
    return middleware