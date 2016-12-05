from django.db.models.signals import m2m_changed, post_save
from django.conf import settings
from django.contrib.auth.models import User
from django.dispatch import receiver

from musette.models import AbstractProfile, Forum


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


@receiver(m2m_changed, sender=Forum.moderators.through)
def post_save_forum(sender, instance, **kwargs):
    """
    This signal is event of model forum for add permissions
    """
    # If add moderator
    if kwargs['action'] == 'post_add':
        for moderator in instance.moderators.all():
            # Superuser not is necessary
            if not moderator.is_superuser:
                instance.add_permissions_topic_moderator(moderator)

    # If remove moderator
    elif kwargs['action'] == 'post_remove':
        ids_removed = kwargs['pk_set']
        for id in ids_removed:
            old_moderator = User.objects.get(id=id)
            # Superuser not is necessary
            if not old_moderator.is_superuser:
                # Only remove permissions if moderator has one forum
                if instance.tot_forums_moderators(old_moderator) <= 1:
                    instance.clear_permissions_moderator(old_moderator)
