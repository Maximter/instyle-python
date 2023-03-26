import os, errno
import re
from django.core.files.storage import FileSystemStorage
from django.utils.crypto import get_random_string
from sorl.thumbnail import ImageField, get_thumbnail
from django.core.files.move import file_move_safe
from sorl.thumbnail import delete


from post.models import Post

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