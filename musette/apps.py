from django.apps import AppConfig


class MusetteConfig(AppConfig):
    """
    App configuration
    """
    name = 'musette'

    def ready(self):
        # Import signals
        import musette.signals
