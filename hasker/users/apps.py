from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = "hasker.users"
    verbose_name = "Users"

    def ready(self):
        import hasker.users.signals  # noqa F401
