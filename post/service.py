import os
from django.core.files.storage import FileSystemStorage
from django.utils.crypto import get_random_string

def check_valid_post(file, comment):
    if file is None:
        return {
            'valid': False,
            'err': 'Файл не был загружен',
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

def upload_post(file, user):
    fs = FileSystemStorage(location=f'static/img/big/post/{user.id}')
    id_post = get_random_string(length=12)
    filename, file_extension = os.path.splitext(file.name)
    print (file_extension)
    if file_extension == '.gif':
        fs.save(f'{id_post}.gif', file)
    elif file_extension == '.mp4':
        fs.save(f'{id_post}.mp4', file)
    else:
        fs.save(f'{id_post}.jpg', file)
    return id_post

def save_post_to_db(id_post, comment, user):
    return