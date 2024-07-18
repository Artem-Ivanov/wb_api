import structlog
from django.apps import AppConfig
from django.conf import settings
from django.contrib.auth import get_user_model


logger = structlog.getLogger(__name__)

USERNAME = "admin"
EMAIL = "admin@1cupis.ru"
PASSWORD = "admin"


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.core"

    def ready(self):
        if not any(["stage" in settings.NAMESPACE, settings.DEBUG]):
            logger.info("Admin user creating not allowed.")
            return

        user_model = get_user_model()

        try:
            user, created = user_model.objects.get_or_create(
                username=USERNAME,
                email=EMAIL,
                is_superuser=True,
                is_staff=True,
            )

            if created:
                user.set_password(PASSWORD)
                user.save()
                logger.info("Admin user successfully created.")
            else:
                logger.info("Admin user already exists.")
        except Exception as exc:
            logger.exception(f"{type(exc).__name__}: {exc}")
