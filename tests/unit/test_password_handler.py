import pytest

from src.utils.password_handler import password_hasher

pytestmark = pytest.mark.unit


def test_hash_and_verify():
    hashed = password_hasher.hash("securepassword")
    assert password_hasher.verify("securepassword", hashed)
    assert not password_hasher.verify("wrongpassword", hashed)


def test_hash_is_not_plaintext():
    assert password_hasher.hash("securepassword") != "securepassword"
