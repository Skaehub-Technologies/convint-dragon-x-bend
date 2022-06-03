from .base import *


if config("ENV_NAME") == 'Production':
    from .production import *
elif config("ENV_NAME") == 'Staging':
    from .staging import *
else:
    from .local import *