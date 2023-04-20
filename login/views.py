from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import redirect
from django.contrib import messages

from signup.models import Token, User
from .service import check_user_exist, get_token, send_mail_func


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
 
def confirm(request):
    key = request.GET['key']
    token = get_object_or_404(Token, confirmation_key=key)
    token.confirmation_key = ''
    token.save()
    User.objects.filter(id=token.user.id).update(verificated=True)
    messages.success(request, 'Регистрация подтверждена. Теперь Вы можете войти.')
    return redirect('/login')