from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import csrf_protect
from .models import User
from .service import valid_user, create_user


def index(request):
    page = loader.get_template('signup/index.html')
    response = HttpResponse(page.render(request=request))
    response.delete_cookie('instyle_token')
    return response

@csrf_protect
def create(request):
    user: User = {
        'email': request.POST.get('email').strip(),
        'name_lastname': request.POST.get('name_lastname').strip(),
        'username': request.POST.get('username').strip(),
        'password': request.POST.get('password').strip(),
    }

    err_valid_user = valid_user(user)
    if err_valid_user:
        return render(request, 'signup/index.html', context={'err': err_valid_user})
    else: create_user(user)
    #TODO Отправить письмо, подтверждающее почту
    return render(request, 'signup/index.html', context={'success': True})
