from django.shortcuts import render


def index(request):
    icecreams = ''
    friends = ''
    city_weather = ''
    friend_output = ''

    context = {
        'icecreams': icecreams,
        'friends': friends,
        'friend_output': friend_output,
        'city_weather': city_weather,
    }
    return render(request, 'signup/index.html', context)
