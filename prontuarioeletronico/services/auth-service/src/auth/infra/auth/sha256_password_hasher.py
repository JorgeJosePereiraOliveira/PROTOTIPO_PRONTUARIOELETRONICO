import hashlib

from ...application.auth.contracts import PasswordHasher


class Sha256PasswordHasher(PasswordHasher):
    def hash(self, plain_password: str) -> str:
        return hashlib.sha256(plain_password.encode("utf-8")).hexdigest()

    def verify(self, plain_password: str, password_hash: str) -> bool:
        return self.hash(plain_password) == password_hash
