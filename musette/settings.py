from django.conf import settings

SITE_NAME = getattr(settings, "SITE_NAME", "Musette")
