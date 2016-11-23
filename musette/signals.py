from django.db.models.signals import post_save
from django.conf import settings
from django.contrib.auth.models import User
from django.dispatch import receiver

from musette.models import AbstractProfile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def post_save_user(sender, instance, **kwargs):
    """
    This signal is event of model user for create new profile
    """
    if kwargs['created']:
        subclasses = AbstractProfile.__subclasses__()
        if len(subclasses) > 0:
            user = User.objects.get(id=instance.id)
            Profile = subclasses[0]
            profile = Profile(iduser=user)
            profile.save()
