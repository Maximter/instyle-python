from signup.models import Token, User

def get_user_by_token(token):
    try:
        token_model = Token.objects.get(token=token)
    except Token.DoesNotExist:
        return None
    return token_model.user

def get_owner(username):
    try:
        owner = User.objects.get(username=username)
    except User.DoesNotExist:
        return None
    return owner