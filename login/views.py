from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import redirect
from django.contrib import messages
from settings.views import forgot_password
import uuid
from signup.models import Token, User
from signup.service import save_yandex_user
from .service import check_user_exist, get_token, get_yandex_token, get_yandex_user, save_new_password, valid_password


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


def yandex(request):
    code = request.GET['code']
    tokens = get_yandex_token(code)
    yandex_user = get_yandex_user(tokens)
    try:
        user = User.objects.get(email=yandex_user['default_email'])
    except User.DoesNotExist:
        user = save_yandex_user(yandex_user)
        messages.success(request, 'Вы были успешно зарегистрированы. Временный пароль был отправлен на эл. почту. Для изменения пароля зайдите в настройки приложения')
    response = HttpResponseRedirect('/')
    response.set_cookie(key='instyle_token', value=get_token(user))
    return response


def confirm(request):
    key = request.GET['key']
    token = get_object_or_404(Token, confirmation_key=key)
    token.confirmation_key = ''
    token.save()
    User.objects.filter(id=token.user.id).update(verificated=True)
    messages.success(request, 'Регистрация подтверждена. Теперь Вы можете войти')
    return redirect('/login')


def forgot_password_page(request):
    key = request.GET['key']
    get_object_or_404(Token, confirmation_key=key)
    return render(request, 'settings/change-password.html', context={'key': key})


def change_password(request):
    key = request.POST.get('key')
    password = request.POST.get('password')
    err_password = valid_password(password)
    if err_password is not None:
        messages.error(request, err_password)
        return redirect(f'/login/change-forgot-password-page/?key={key}')
    token = get_object_or_404(Token, confirmation_key=key)
    save_new_password(token.user, password)
    token.confirmation_key = ''
    token.token = uuid.uuid4()
    token.save()
    messages.success(request, 'Пароль был изменён')
    return redirect('/login')


def login_enter_email(request):
    return render(request, 'login/email-forgot-password.html')


def login_change_email(request):
    username = request.POST.get('username')
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        messages.error(request, 'Введён неверное имя пользователя')
        return redirect('/login/login-forgot-password')
    return forgot_password(request, user)
