from django.conf import settings

SITE_NAME = getattr(settings, "SITE_NAME", "Musette")

# Name of app profile
APP_PROFILE = getattr(settings, "APP_PROFILE", "profiles")
MODEL_PROFILE = getattr(settings, "MODEL_PROFILE", "Profile")
FIELD_PHOTO_PROFILE = getattr(settings, "FIELD_PHOTO_PROFILE", "photo")

URL_PROFILE = getattr(settings, "URL_PROFILE", "/profile/")

# Parameter/s that necessary for URL PROFILE.
# Field of model profile that use with parameter/s
FIELDS_PARAMS = ("username",)
URL_PROFILE_PARAMS = getattr(settings, "URL_PROFILE_PARAMS", FIELDS_PARAMS)
