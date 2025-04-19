from django.apps import AppConfig


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
    verbose_name = 'App'

    def ready(self):
        import app.models.signals  # noqa: F401
        import app.admin  # noqa: F401
