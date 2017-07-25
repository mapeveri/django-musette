from django.contrib.auth import get_user_model


def create_user(username, email, password):
    User = get_user_model()
    user = User.objects.create_user(
        username, email, password
    )
    user.save()
