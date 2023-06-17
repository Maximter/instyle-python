from django.shortcuts import redirect, render
from login.service import send_mail_func

from signup.service import create_user_and_token
from .forms import SignupForm
from django.contrib import messages
from django.contrib.auth.hashers import make_password


def signup_index(request):
    form = SignupForm()
    response = render(request, 'signup/index.html', {'form': form})
    response.delete_cookie('instyle_token')
    return response


def create(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = create_user_and_token(form)
            send_mail_func(user)
            messages.success(request, 'Для завершения регистрации, была выслана ссылка на эл. адрес для его подтверждения')
            return redirect('/')
    else:
        form = SignupForm()
    
    return render(request, 'signup/index.html', context={'form': form })
