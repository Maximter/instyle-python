from django.http import HttpResponse
from django.shortcuts import render

from post.service import check_valid_post, delete_post_from_db, get_model_post, get_post_interaction, get_user_post_interaction, save_like, save_post_to_db, upload_post
from user.service import get_user_by_token

def index(request):
    user = get_user_by_token(request.COOKIES.get('instyle_token'))
    return render(request, 'post/index.html', context={'user':user})


def create(request):
    comment = request.POST.get('comment')
    if comment is not None:
        comment = comment.strip() 
    user = get_user_by_token(request.COOKIES.get('instyle_token'))

    if request.method == 'POST' and request.FILES:
        file = request.FILES['photo'] 

        valid_post = check_valid_post(file, comment)
        if not valid_post['valid']:
            return render(request, 'post/index.html', context={'err': valid_post['err'], 'comment': comment})
        
        id_post = upload_post(file, user)
        save_post_to_db(id_post, comment, user)
        return render(request, 'post/index.html', context={'user':user, 'success': 'Пост будет опубликован через несколько секунд'})
    return render(request, 'post/index.html', context={'user':user, 'err': 'Ошибка файла', 'comment': comment})


def post_page(request, id_post):
    model_post = get_model_post(id_post)
    if model_post is None:
        return render(request, 'error/404.html')
    user = get_user_by_token(request.COOKIES.get('instyle_token'))
    model_post.interaction = get_post_interaction(model_post)
    if user is not None:
        user.owner = user.id == model_post.user.id
        user.post_interaction = get_user_post_interaction(user, model_post)
    return render(request, 'post/post_page.html', context={'user':user, 'post':model_post})


def like_post(request, id_post):
    user = get_user_by_token(request.COOKIES.get('instyle_token'))
    save_like(user, id_post)
    return HttpResponse()


def delete_post(request, id_post):
    user = get_user_by_token(request.COOKIES.get('instyle_token'))
    delete_post_from_db(user, id_post)
    return HttpResponse()
