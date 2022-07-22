from django.core.exceptions import ValidationError
from django.test import TestCase
from app.user.validators import (
    validate_password_digit,
    validate_password_lowercase,
    validate_password_symbol,
    validate_password_uppercase,
)

class ValidatorsTest(TestCase):

    def test_user_password_validator_digit(self) -> None:
        with self.assertRaises(ValidationError):
            validate_password_digit("Kloanda-ka")

    def test_user_password_validator_uppercase(self) -> None:
        with self.assertRaises(ValidationError):
            validate_password_uppercase("kloanada-13")

    def test_user_password_validator_lowercase(self) -> None:
        with self.assertRaises(ValidationError):
            validate_password_lowercase("KLOANADA-13")

    def test_user_password_validator_symbol(self) -> None:
        with self.assertRaises(ValidationError):
            validate_password_symbol("Kloanada134")