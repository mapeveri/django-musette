from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.http import Http404
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


class RestrictStaffToAdminMiddleware(object):
    """
    A middleware that restricts staff members
    access to administration panels
    """
    def process_request(self, request):
        if request.path.startswith(reverse('admin:index')):
            if request.user.is_authenticated():
                if not request.user.is_staff:
                    raise Http404
            else:
                raise Http404
