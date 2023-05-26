import json
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from notification.service import send_notification
from post.models import Favorite

from post.service import delete_comment_from_db, delete_post_from_db, edit_comment_db, edit_visibility_db, get_model_post, get_post_interaction, get_post_interaction_by_id, get_user_like, save_like, send_comment_db, update_hide_comment, update_hide_like, update_post_comment_db
from signup.models import UserProfile
from user.service import get_user_by_token, is_follower


def post_page(request, id_post):
    model_post = get_model_post(id_post)
    if model_post is None:
        return render(request, 'error/404.html')
    user = get_user_by_token(request.COOKIES.get('instyle_token'))
    profile = UserProfile.objects.get(user=user)
    model_post.interaction = get_post_interaction(model_post)
    if user is not None:
        user.owner = user.id == model_post.user.id
        user.like = get_user_like(user, model_post)
        if not user.owner:
            if model_post.visibility == 'nobody':
                return render(request, 'error/404.html')
            elif model_post.visibility == 'follower' and not is_follower(user, model_post.user):
                return render(request, 'error/404.html')
    elif not model_post.visibility == 'all':
        return render(request, 'error/404.html')
    owner_profile = UserProfile.objects.get(user=model_post.user.id)
    try:
        Favorite.objects.get(user=user, post=model_post)
        favorite = True
    except Favorite.DoesNotExist:
        favorite = False
    # TODO если видео, то mp4 = True
    # print(os.path.exists(f'{settings.BASE_DIR}/static/img/video/{user.id}/{model_post.id}.mp4'))
    return render(request, 'post/post_page.html', context={'user': user, 'post': model_post, 'profile': profile, 'owner_profile': owner_profile, 'favorite':favorite})


def like_post(request, id_post):
    user = get_user_by_token(request.COOKIES.get('instyle_token'))
    save_like(user, id_post)
    return HttpResponse()


def delete_post(request, id_post):
    user = get_user_by_token(request.COOKIES.get('instyle_token'))
    delete_post_from_db(user, id_post)
    return HttpResponse()


def update_post_comment(request, id_post):
    comment = get_comment(request)
    if len(comment) < 10 or len(comment) > 1500:
        return
    model_post = get_model_post(id_post)
    user = get_user_by_token(request.COOKIES.get('instyle_token'))

    if model_post.user.id != user.id:
        return

    update_post_comment_db(model_post, comment)
    return HttpResponse()


def send_comment(request, id_post):
    comment = get_comment(request)
    if len(comment) < 2 or len(comment) > 1500:
        return
    model_post = get_model_post(id_post)
    user = get_user_by_token(request.COOKIES.get('instyle_token'))
    send_notification(model_post.user, user, 'comment', model_post)
    send_comment_db(user, model_post, comment)
    return HttpResponse()


def add_favorite(request, id_post):
    user = get_user_by_token(request.COOKIES.get('instyle_token'))
    model_post = get_model_post(id_post)
    favorite, created = Favorite.objects.get_or_create(user=user, post=model_post)

    if created:
        favorite.save()
    else:
        favorite.delete()

    return HttpResponse()

def edit_comment(request, id_interaction):
    comment = get_comment(request)
    user = get_user_by_token(request.COOKIES.get('instyle_token'))
    model_interaction = get_post_interaction_by_id(id_interaction)
    if model_interaction.user != user:
        return None
    edit_comment_db(model_interaction, comment)
    return HttpResponse()


def delete_comment(request, id_comment):
    user = get_user_by_token(request.COOKIES.get('instyle_token'))
    delete_comment_from_db(user, id_comment)
    return HttpResponse()


def hide_like(request, id_post):
    user = get_user_by_token(request.COOKIES.get('instyle_token'))
    model_post = get_model_post(id_post)
    if model_post.user != user:
        return
    update_hide_like(model_post)
    return HttpResponse()


def hide_comment(request, id_post):
    user = get_user_by_token(request.COOKIES.get('instyle_token'))
    model_post = get_model_post(id_post)
    if model_post.user != user:
        return
    update_hide_comment(model_post)
    return HttpResponse()


def edit_visibility(request, id_post):
    body_unicode = request.body.decode('utf-8')
    body_data = json.loads(body_unicode)
    visibility = body_data['visibility']
    user = get_user_by_token(request.COOKIES.get('instyle_token'))
    model_post = get_model_post(id_post)
    if model_post.user != user:
        return None
    edit_visibility_db(model_post, visibility)
    return HttpResponse()


def get_comment(request):
    body_unicode = request.body.decode('utf-8')
    body_data = json.loads(body_unicode)
    return body_data['comment']
