import os, errno
import re
from django.core.files.storage import FileSystemStorage
from django.utils.crypto import get_random_string
from sorl.thumbnail import get_thumbnail
from django.core.files.move import file_move_safe
from django.db.models import Case, Value, When
from django.db.models import Q


from post.models import Post, Post_interaction

def check_valid_post(file, comment):
    if file is None:
        return {
            'valid': False,
            'err': 'Файл не был загружен',
        }
    
    filename, file_extension = os.path.splitext(file.name)
    match = re.match('\.(jpg|JPG|jpeg|JPEG|png|PNG|mp4)$', file_extension)
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

    if file_extension == '.mp4':
        fs = FileSystemStorage(location=f'static/img/video/{user.id}')
        fs.save(f'{id_post}.mp4', file)
    else:
        fs = FileSystemStorage(location=f'static/img/big/post/{user.id}')
        fs.save(f'{id_post}.jpg', file)
        upload_in_other_qualities(id_post, user.id)
    return id_post

def save_post_to_db(id_post, comment, user):
    Post.objects.create_post(id_post= id_post, comment=comment, user=user)
    return

def save_like(user, id_post):
    model_post = get_model_post(id_post)
    try:
        interactions = Post_interaction.objects.filter(post=model_post.id, user=user.id)
        if len(interactions) == 0:
            raise Post_interaction.DoesNotExist
        interactions.update(like=Case(
            When(like=True, then=Value(False)),
            When(like=False, then=Value(True)),
        ))
    except Post_interaction.DoesNotExist:
        Post_interaction.objects.create_like(user= user, post=model_post)
    
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
            'info': Post_interaction.objects.filter(post=post.id, comment=Q(comment='')),
            'like_count': len(Post_interaction.objects.filter(post=post.id, like=True))
        }
    except Post_interaction.DoesNotExist:
        return None

def get_post_interaction_by_id(id_interaction):
    try:
        return Post_interaction.objects.get(id=id_interaction)
    except Post_interaction.DoesNotExist:
        return None

def edit_comment_db(interaction, comment):
    return Post_interaction.objects.filter(id=interaction.id).update(comment=str(comment))

def get_user_post_interaction(user, post):
    try:
        return Post_interaction.objects.get(user=user.id, post=post.id)
    except Post_interaction.DoesNotExist:
        return None

def get_model_post(id_post):
    try:
        model_post = Post.objects.get(id_post=id_post)
    except Post.DoesNotExist:
        return None
    return model_post

def send_comment_db(user, post, comment):
    try:
        interactions = Post_interaction.objects.filter(post=post.id, user=user.id)
        if len(interactions) == 0:
            raise Post_interaction.DoesNotExist
        interactions.update(comment=comment)
    except Post_interaction.DoesNotExist:
        Post_interaction.objects.create_comment(user= user, post=post, comment=comment)
    
    return

def delete_comment_from_db(user, id_interaction):
    try:
        model_interaction = Post_interaction.objects.filter(id=id_interaction)
    except Post.DoesNotExist:
        return None

    if user.id != model_interaction[0].user.id and model_interaction[0].post.user.id != user.id:
        return None
    
    model_interaction.update(comment='')
    return

def update_hide_like(post):
    try:
        model_post = Post.objects.filter(id=post.id,)
        if len(model_post) == 0:
            raise Post_interaction.DoesNotExist
        model_post.update(hide_like=Case(
            When(hide_like=True, then=Value(False)),
            When(hide_like=False, then=Value(True)),
        ))
    except Post_interaction.DoesNotExist:
        return None
    return

def update_hide_comment(post):
    try:
        model_post = Post.objects.filter(id=post.id,)
        if len(model_post) == 0:
            raise Post_interaction.DoesNotExist
        model_post.update(hide_comment=Case(
            When(hide_comment=True, then=Value(False)),
            When(hide_comment=False, then=Value(True)),
        ))
    except Post_interaction.DoesNotExist:
        return None
    return