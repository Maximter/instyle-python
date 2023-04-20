from django.shortcuts import render

from post.service import check_valid_post, save_post_to_db, upload_post
from signup.models import UserProfile
from user.service import get_user_by_token
from django.shortcuts import redirect
from django.contrib import messages

def index(request):
    user = get_user_by_token(request.COOKIES.get('instyle_token'))
    profile = UserProfile.objects.get(user=user)
    return render(request, 'post/index.html', context={'user':user, 'profile':profile})


def create(request):
    comment = request.POST.get('comment')
    if comment is not None:
        comment = comment.strip() 
    user = get_user_by_token(request.COOKIES.get('instyle_token'))

    if request.method == 'POST' and request.FILES:
        file = request.FILES['photo'] 

        valid_post = check_valid_post(file, comment)
        if valid_post['err']:
            messages.error(request, valid_post['err'])
            return redirect('/post')
        
        id_post = upload_post(file, user)
        save_post_to_db(id_post, comment, user)
        messages.success(request, 'Пост будет опубликован через несколько секунд')
        return redirect('/post')
    messages.error(request, 'Ошибка файла')
    return redirect('/post')

