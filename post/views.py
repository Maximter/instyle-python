from django.shortcuts import render

from post.service import check_valid_post, save_post_to_db, upload_post
from signup.models import UserProfile
from user.service import get_user_by_token

def index(request):
    user = get_user_by_token(request.COOKIES.get('instyle_token'))
    profile = UserProfile.objects.get(user=user)
    return render(request, 'post/index.html', context={'user':user, 'profile':profile})


def create(request):
    comment = request.POST.get('comment')
    if comment is not None:
        comment = comment.strip() 
    user = get_user_by_token(request.COOKIES.get('instyle_token'))
    profile = UserProfile.objects.get(user=user)

    if request.method == 'POST' and request.FILES:
        file = request.FILES['photo'] 

        valid_post = check_valid_post(file, comment)
        if not valid_post['valid']:
            return render(request, 'post/index.html', context={'user':user,'err': valid_post['err'], 'comment': comment, 'profile':profile})
        
        id_post = upload_post(file, user)
        save_post_to_db(id_post, comment, user)
        return render(request, 'post/index.html', context={'user':user, 'success': 'Пост будет опубликован через несколько секунд', 'profile':profile})
    return render(request, 'post/index.html', context={'user':user, 'err': 'Ошибка файла', 'comment': comment, 'profile':profile})
