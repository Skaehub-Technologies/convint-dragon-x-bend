from typing import Any

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_bytes


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp) -> Any:  # type: ignore
        return (
            smart_bytes(user.pk)
            + smart_bytes(timestamp)
            + smart_bytes(user.is_verified)
        )


account_activation_token = TokenGenerator()
