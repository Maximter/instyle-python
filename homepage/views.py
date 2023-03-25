from django.shortcuts import render
from user.service import get_user_by_token

def index(request):
    user = get_user_by_token(request.COOKIES.get('instyle_token'))
    context = {
        'user': user
    }
    return render(request, 'homepage/index.html', context)

    # const user = await this.appService.getUser(req);
    # const postsInfo = await this.appService.getPosts(user);
    # const posts = await this.appService.getLikes(user, postsInfo);
    # let recommendation;
    # if (posts == undefined) {
    #   const countLikes = await this.recommendstionService.getPopularPosts();
    #   const popularPostsInfo = await this.recommendstionService.getPopularPostsFullData(countLikes);
    #   recommendation = await this.appService.getLikes(user, popularPostsInfo);
    # }
  
    # return res.render('index', { user: user, posts: posts, recommendation : recommendation });
