from django.apps import AppConfig

class ContentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'content'

    def ready(self):
        """
        Override the ready() method to import the signals module, which will
        register the signals with the corresponding receivers. This is a
        one-time operation that happens when the app is ready.
        """
        
        import content.signals