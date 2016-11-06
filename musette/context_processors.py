from django.conf import settings

from .models import Configuration
from .utils import get_notifications


def data_templates(request):
    """
    context_processors for get in all templates
    """
    # Get notifications data
    notifications = get_notifications(request.user.id)

    # Get configurations
    try:
        configurations = Configuration.objects.all()[:1].get()
    except Configuration.DoesNotExist:
        configurations = None

    return {
        'SETTINGS': settings,
        'notifications': notifications,
        'configurations': configurations
    }
