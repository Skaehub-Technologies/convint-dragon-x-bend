from decouple import config

from .base import *  # noqa

if config("ENV_NAME") == "Production":  # noqa
    from .production import *  # noqa
elif config("ENV_NAME") == "Staging":
    from .staging import *  # noqa
else:
    from .local import *  # noqa
