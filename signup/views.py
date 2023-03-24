from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from .models import User
from .service import valid_user, create_user


def index(request):
    return render(request, 'signup/index.html')

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
    
    return render(request, 'signup/index.html', context={'success': True})
