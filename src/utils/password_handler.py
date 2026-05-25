from argon2 import PasswordHasher as NativeHasher
from argon2.exceptions import VerifyMismatchError


class PasswordHasher:
    def __init__(self):
        self._hasher = NativeHasher()

    def hash(self, plain_password: str) -> str:
        return self._hasher.hash(plain_password)

    def verify(self, plain_text: str, hashed_password: str) -> bool:
        try:
            return self._hasher.verify(hashed_password, plain_text)
        except VerifyMismatchError:
            return False


password_hasher = PasswordHasher()
