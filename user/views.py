from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .service import get_posts, get_user_by_token, get_owner

def index(request):
    response = HttpResponseRedirect('/')
    return response

def user_page(request, username):
    user = get_user_by_token(request.COOKIES.get('instyle_token'))
    owner = get_owner(username)
    if owner is None:
        return render(request, 'error/404.html')
    
    if user.id == owner.id:
        user.owner = True
    # else:
        # const follow = await this.userService.isFollow(user, owner);
        #   if (follow) user['follow'] = true;

    # const follows = await this.userService.getfollows(owner);
    posts = get_posts(owner)
    if posts is not None:
        owner.countPost = len(posts)
    # owner['followers'] = follows['follower'];
    # owner['followings'] = follows['following'];
    # owner['countFollowers'] = follows['follower'].length;
    # owner['countFollowings'] = follows['following'].length;
    # if (owner['online'] == '0') owner['onlineBool'] = true;   

    context = {
        'user': user,
        'owner': owner,
        'posts': posts,
    }
    return render(request, 'user/index.html', context)
