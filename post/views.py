from django.shortcuts import render

from post.service import check_valid_post, save_post_to_db, upload_post
from user.service import get_user_by_token

# Create your views here.
def index(request):
    return render(request, 'post/index.html')

def create(request):
    if request.method == 'POST' and request.FILES:
        file = request.FILES['photo']
        comment = request.POST.get('comment').strip()

        valid_post = check_valid_post(file, comment)
        if not valid_post['valid']:
            return render(request, 'post/index.html', context={'err': valid_post['err']})
        
        user = get_user_by_token(request.COOKIES.get('instyle_token'))
        id_post = upload_post(file, user)
        save_post_to_db(id_post, comment, user)

    return render(request, 'post/index.html', context={'user':user, 'success': 'Пост будет опубликован через несколько секунд'})
