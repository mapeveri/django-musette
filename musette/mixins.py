from django.utils.decorators import method_decorator
from musette.decorators import user_is_troll


class UserTrollMixin(object):
    """
    Mixin for check if the user is a troll.
    """
    @method_decorator(user_is_troll)
    def dispatch(self, *args, **kwargs):
        return super(UserTrollMixin, self).dispatch(*args, **kwargs)
