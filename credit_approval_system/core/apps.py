from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field='django.db.models.BigAutoField'
    name='core'

    def ready(self):
        from .tasks import load_initial_data
        # load_initial_data.delay()