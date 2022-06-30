from typing import Any

import six
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp) -> Any:  # type: ignore
        return (
            six.text_type(user.pk)
            + six.text_type(timestamp)
            + six.text_type(user.is_verified)
        )


account_activation_token = TokenGenerator()
