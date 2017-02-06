from django.db.models.signals import m2m_changed, pre_delete, post_save
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver

from musette import models, utils


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def post_save_user(sender, instance, **kwargs):
    """
    This signal is event of model user for create new profile
    """
    if kwargs['created']:
        subclasses = models.AbstractProfile.__subclasses__()
        if len(subclasses) > 0:
            User = get_user_model()
            user = User.objects.get(id=instance.id)
            Profile = subclasses[0]

            # For confirm email
            data = utils.get_data_confirm_email(user.email)

            # Insert profile
            profile = Profile(
                iduser=user, photo="", about="",
                activation_key=data['activation_key'],
                key_expires=data['key_expires']
            )
            profile.save()

            # Send email for confirm user
            utils.send_welcome_email(
                user.email, user.username, data['activation_key']
            )


@receiver(m2m_changed, sender=models.Forum.moderators.through)
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
            User = get_user_model()
            old_moderator = User.objects.get(id=id)
            # Superuser not is necessary
            if not old_moderator.is_superuser:
                # Only remove permissions if moderator has one forum
                if instance.tot_forums_moderators(old_moderator) < 1:
                    instance.clear_permissions_moderator(old_moderator)


@receiver(pre_delete, sender=models.Topic)
@receiver(pre_delete, sender=models.Comment)
def pre_delete_receiver_notification(sender, instance, **kwargs):
    """
    Delete notification comment or topic
    """
    ctype = ContentType.objects.get_for_model(instance)
    models.Notification.objects.filter(
        content_type=ctype, idobject=instance.pk
    ).delete()
