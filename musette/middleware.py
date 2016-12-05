from django.core.cache import cache
from django.utils import timezone

from . import settings


class ActiveUserMiddleware(object):
    """
    Set user authenticate
    """
    def process_request(self, request):
        current_user = request.user
        if request.user.is_authenticated():
            now = timezone.now()
            cache.set(
                'seen_%s' % (current_user.username), now,
                settings.USER_LASTSEEN_TIMEOUT
            )