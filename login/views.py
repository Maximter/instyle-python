from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from signup.models import User
from .service import check_user_exist, get_token


def index(request):
    page = loader.get_template('login/index.html')
    response = HttpResponse(page.render(request=request))
    response.delete_cookie('instyle_token')
    return response

@csrf_protect
def login(request):
    user: User = {
        'username': request.POST.get('username').strip(),
        'password': request.POST.get('password').strip(),
    }

    user_exist = check_user_exist(user)
    if not user_exist['valid']:
        context = {
            'err': user_exist['err'],
            'warn': user_exist['warn'],
            'user': user_exist['user'] 
        }
        return render(request, 'login/index.html', context=context,)
    
    response = HttpResponseRedirect('/')
    response.set_cookie(key='instyle_token', value=get_token(user_exist['user_model']))
    return response
 