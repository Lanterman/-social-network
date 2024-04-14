import string
import hashlib

from secrets import choice

from django.core.exceptions import ValidationError

from .models import User


# User password
# to password hashing
def create_salt(length: int = 12) -> str:
    """Create a random string"""

    return "".join(choice(string.ascii_letters) for _ in range(length))


def password_hashing(password: str, salt: str | None = None) -> str:
    """Hashing a user password"""

    if not salt:
        salt = create_salt()

    enc = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)

    return enc.hex()


def create_hashed_password(password: str) -> str:
    """Create a hashed_password field of a User model instance"""

    salt = create_salt()
    hashed = password_hashing(password, salt)
    return f"{salt}${hashed}"


# Check if the login password and the existing password are the same
class ValidateCustomPassword:
    """Validate custom password"""

    error_mes = "Please enter a correct username and password. Note that both fields may be case-sensitive."

    def __init__(self, error_mes = None) -> None:
        self.error_mes = error_mes or ValidateCustomPassword.error_mes
    
    @staticmethod
    def validate_password(password: str, hashed_password: str) -> bool:
        """Check if the password matches the hashed password from database"""

        salt, hashed = hashed_password.split("$")
        return password_hashing(password, salt) == hashed
    
    def check_custom_password(self, field_key: str, user: User, form) -> None:
        """Check a custom password"""

        if not self.validate_password(form.data[field_key], user.hashed_password):
            form.add_error("__all__", ValidationError(self.error_mes, "invalid"))
