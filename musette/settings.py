from django.conf import settings

APP_PROFILE = getattr(settings, 'APP_PROFILE', "profiles")
MODEL_PROFILE = getattr(settings, 'MODEL_PROFILE', "profile")
FIELD_PHOTO_PROFILE = getattr(settings, 'FIELD_PHOTO_PROFILE', "photo")

URL_PROFILE = getattr(settings, 'URL_PROFILE', "/profile/")