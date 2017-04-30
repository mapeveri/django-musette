from django.http import HttpResponseRedirect


def user_is_troll(f):
    """
    Decorator for check if the user is a troll.

    Args:
        f (function): Function to decorated.

    Returns:
        function: wrap function.
    """
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated():
            is_troll = request.user.user.is_troll
            if not is_troll:
                return f(request, *args, **kwargs)
            else:
                return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/')
    return wrap
