from decouple import config

from .base import *  # noqa F403, F401

if config("ENV_NAME") == "Production":  # noqa F403, F401
    from .production import *  # noqa F403, F401
elif config("ENV_NAME") == "Staging":
    from .staging import *  # noqa F403, F401
else:
    from .local import *  # noqa F403, F401
