from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = "hasker.users"
    verbose_name = "Users"

    def ready(self):
        try:
            import hasker.users.signals  # noqa F401
        except ImportError:
            pass
