import json
import os
import errno
import re
import io
import urllib.request
from django.core.files.storage import FileSystemStorage
from django.utils.crypto import get_random_string
import requests
from sorl.thumbnail import get_thumbnail
from django.core.files.move import file_move_safe
from django.db.models import Case, Value, When
from django.core.files import File
from instyle import settings
from notification.service import delete_notification, send_notification
from post.models import Comment, Like, Post
import shutil


def check_valid_post(file, comment):
    if file is None:
        return {
            'valid': False,
            'err': 'Файл не был загружен',
        }

    filename, file_extension = os.path.splitext(file.name)
    match = re.match('\.(jpg|JPG|jpeg|JPEG|png|PNG)$', file_extension)
    if not match:
        return {
            'valid': False,
            'err': 'Неверный формат файла',
        }
    elif file.size > 1024 * 1024 * 150:
        return {
            'valid': False,
            'err': 'Слишком большой размер файла. Максимальный размер файла: 150Мб',
        }
    elif len(comment) > 1500:
        return {
            'valid': False,
            'err': 'Слишком длинное описание файла. Максимальный размер комментария: 1500 символов',
        }
    else:
        return {
            'valid': True,
            'err': '',
        }


def upload_in_other_qualities(id_post, id_user):
    medium_file = get_thumbnail(f'static/img/big/post/{id_user}/{id_post}.jpg', '1200', quality=99, format='JPEG')
    small_file = get_thumbnail(f'static/img/big/post/{id_user}/{id_post}.jpg', '500', quality=99, format='JPEG')

    try:
        os.mkdir(f'static/img/medium/post/{id_user}')
    except OSError as err:
        if err.errno != errno.EEXIST:
            pass
    try:
        os.mkdir(f'static/img/small/post/{id_user}')
    except OSError as err:
        if err.errno != errno.EEXIST:
            pass

    file_move_safe(medium_file.name, f'static/img/medium/post/{id_user}/{id_post}.jpg')
    file_move_safe(small_file.name, f'static/img/small/post/{id_user}/{id_post}.jpg')
    return


def upload_post(file, user):
    id_post = get_random_string(length=12)
    filename, file_extension = os.path.splitext(file.name)

    fs = FileSystemStorage(location=f'static/img/big/post/{user.id}')
    fs.save(f'{id_post}.jpg', file)
    upload_in_other_qualities(id_post, user.id)
    return id_post


def get_image_keywords(user, post_id):
    api_key = settings.IMAGGA_API_KEY
    api_secret = settings.IMAGGA_API_SECRET

    response = requests.post(
    'https://api.imagga.com/v2/tags?threshold=50',
    auth=(api_key, api_secret),
    files={'image': open(f'{settings.BASE_DIR}/static/img/small/post/{user.id}/{post_id}.jpg', 'rb')})
    keywords = [tag['tag']['en'] for tag in response.json()['result']['tags']]

    return keywords


def save_post_to_db(id_post, comment, user, visibility, keywords):
    Post.objects.create_post(id_post=id_post, comment=comment, user=user, visibility=visibility, keywords=keywords)
    return


def save_like(user, id_post):
    model_post = get_model_post(id_post)
    try:
        like = Like.objects.get(post=model_post.id, user=user.id)
        like.delete()
        delete_notification(model_post.user, user, 'like', model_post)
    except Like.DoesNotExist:
        Like.objects.create_post(user=user, post=model_post)
        if model_post.user != user:
            send_notification(model_post.user, user, 'like', model_post)
    return


def delete_post_from_db(user, id_post):
    model_post = get_model_post(id_post)
    if user.id != model_post.user.id:
        return None
    model_post.delete()
    return


def update_post_comment_db(post, comment):
    return Post.objects.filter(id=post.id).update(comment=comment)


def get_post_interaction(post):
    try:
        return {
            'info': Comment.objects.filter(post=post.id),
            'like_count': len(Like.objects.filter(post=post.id))
        }
    except Comment.DoesNotExist:
        return None
    except Like.DoesNotExist:
        return None


def get_post_interaction_by_id(id_interaction):
    try:
        return Comment.objects.get(id=id_interaction)
    except Comment.DoesNotExist:
        return None


def edit_comment_db(interaction, comment):
    return Comment.objects.filter(id=interaction.id).update(comment_text=str(comment))


def get_user_like(user, post):
    try:
        Like.objects.get(user=user.id, post=post.id)
        return True
    except Like.DoesNotExist:
        return False


def get_model_post(id_post):
    try:
        model_post = Post.objects.get(id_post=id_post)
    except Post.DoesNotExist:
        return None
    return model_post


def send_comment_db(user, post, comment):
    Comment.objects.create_post(user=user, post=post, comment_text=comment)
    return


def delete_comment_from_db(user, id_comment):
    try:
        comment = Comment.objects.get(id=id_comment)
    except Comment.DoesNotExist:
        raise 
    
    if user.id != comment.user.id and comment.post.user.id != user.id:
        return None

    delete_notification(comment.post.user, comment.user, 'comment', comment.post)
    comment.delete()
    return


def edit_visibility_db(post, visibility):
    return Post.objects.filter(id=post.id).update(visibility=str(visibility))


def update_hide_like(post):
    try:
        model_post = Post.objects.filter(id=post.id,)
        if len(model_post) == 0:
            raise Post.DoesNotExist
        model_post.update(hide_like=Case(
            When(hide_like=True, then=Value(False)),
            When(hide_like=False, then=Value(True)),
        ))
    except Post.DoesNotExist:
        return None
    return


def update_hide_comment(post):
    try:
        model_post = Post.objects.filter(id=post.id,)
        if len(model_post) == 0:
            raise Post.DoesNotExist
        model_post.update(hide_comment=Case(
            When(hide_comment=True, then=Value(False)),
            When(hide_comment=False, then=Value(True)),
        ))
    except Post.DoesNotExist:
        return None
    return


def save_posts_from_vk(posts, user):
    all_posts = Post.objects.values_list('id_post', flat=True).filter(user=user.id)
    for post in reversed(posts['response']['items']):
        id_post = post['id']
        if str(id_post) in all_posts:
            continue
        downloaded_max = False
        for size in post['sizes']:
            if size['type'] == 'w' or size['type'] == 'q' or size['type'] == 'y' or size['type'] == 'z':
                response = urllib.request.urlopen(size['url'])
                image = response.read() 
                if size['type'] == 'w':
                    downloaded_max = True
                    fs = FileSystemStorage(location=f'static/img/big/post/{user.id}')
                elif size['type'] == 'y':
                    fs = FileSystemStorage(location=f'static/img/medium/post/{user.id}')
                elif size['type'] == 'z' and not downloaded_max:
                    downloaded_max = True
                    fs = FileSystemStorage(location=f'static/img/big/post/{user.id}')
                else:
                    fs = FileSystemStorage(location=f'static/img/small/post/{user.id}')
                fs.save(f'{id_post}.jpg', File(io.BytesIO(image)))
        
        if not downloaded_max:
            shutil.copyfile(f'static/img/medium/post/{user.id}/{id_post}.jpg', f'static/img/big/post/{user.id}/{id_post}.jpg')
        keywords = get_image_keywords(user, id_post)
        Post.objects.create_post(id_post=id_post, comment='', user=user, keywords=keywords, visibility='all')
    return
