import json
from django.http import HttpResponse
from django.shortcuts import render

from post.service import delete_comment_from_db, delete_post_from_db, edit_comment_db, get_model_post, get_post_interaction, get_post_interaction_by_id, get_user_post_interaction, save_like, send_comment_db, update_post_comment_db
from user.service import get_user_by_token


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


def update_post_comment (request, id_post):
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
    send_comment_db(user, model_post, comment)
    return HttpResponse() 


def edit_comment(request, id_interaction):
    comment = get_comment(request)
    user = get_user_by_token(request.COOKIES.get('instyle_token'))
    model_interaction = get_post_interaction_by_id(id_interaction)
    if model_interaction.user != user:
        return None
    edit_comment_db(model_interaction, comment)
    return HttpResponse() 


def delete_comment(request, id_interaction):
    user = get_user_by_token(request.COOKIES.get('instyle_token'))
    delete_comment_from_db(user, id_interaction)
    return HttpResponse()


def get_comment(request):
    body_unicode = request.body.decode('utf-8')
    body_data = json.loads(body_unicode)
    return body_data['comment']