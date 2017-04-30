from django.apps import AppConfig


class MusetteConfig(AppConfig):
    """
    Musette app configuration.
    """
    name = 'musette'

    def ready(self):
        # Import signals
        import musette.signals
