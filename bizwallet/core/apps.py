from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class CoreConfig(AppConfig):
    name = "bizwallet.core"
    verbose_name = _("Pages")

    def ready(self):
        try:
            import bizwallet.core.signals  # noqa F401
        except ImportError:
            pass
