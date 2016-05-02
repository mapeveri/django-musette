from django.conf import settings

from .utils import get_notifications


def data_templates(request):
    '''
    context_processors for get in all templates
    '''

    # Get notifications data
    notifications = get_notifications(request.user.id)

    return {
        'SETTINGS': settings,
        'notifications': notifications
    }