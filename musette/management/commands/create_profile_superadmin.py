from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from musette.utils import get_main_model_profile, get_data_confirm_email


class Command(BaseCommand):
    help = "Create record profile for SuperAdmin users."

    def handle(self, *args, **options):
        # Get model profile
        Profile = get_main_model_profile()
        # Get users super-admin
        User = get_user_model()
        users = User.objects.filter(is_superuser=True)

        # Create recrod profile
        if users.count() > 0:
            for user in users:
                if not Profile.objects.filter(iduser=user).exists():
                    data = get_data_confirm_email(user.email)
                    Profile.objects.create(
                        iduser=user, photo="", about="",
                        activation_key=data['activation_key'],
                        key_expires=data['key_expires']
                    )
                    self.stdout.write('Profile created: ' + user.username)
                else:
                    self.stdout.write('Profile ' + user.username + ' exists.')
            self.stdout.write("Finished.")
        else:
            self.stdout.write("There is no super-user registered.")
