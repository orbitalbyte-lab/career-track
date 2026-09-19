from app.security.passwords import hash_password, verify_password


def test_hash_password_does_not_return_plain_password():
    password = "TestPassword123!"

    hashed_password = hash_password(password)

    assert hashed_password != password


def test_verify_password_accepts_correct_password():
    password = "TestPassword123!"
    hashed_password = hash_password(password)

    assert verify_password(password, hashed_password) is True


def test_verify_password_rejects_wrong_password():
    password = "TestPassword123!"
    hashed_password = hash_password(password)

    assert verify_password("WrongPassword!", hashed_password) is False


def test_hash_password_generates_different_hashes():
    password = "TestPassword123!"

    first_hash = hash_password(password)
    second_hash = hash_password(password)

    assert first_hash != second_hash