from app.security.passwords import hash_password, verify_password


def test_hash_password_does_not_return_plain_text():
    password = "StrongPassword123!"

    hashed_password = hash_password(password)

    assert hashed_password != password


def test_verify_password_accepts_correct_password():
    password = "StrongPassword123!"

    hashed_password = hash_password(password)

    assert verify_password(password, hashed_password) is True


def test_verify_password_rejects_incorrect_password():
    password = "StrongPassword123!"
    wrong_password = "WrongPassword123!"

    hashed_password = hash_password(password)

    assert verify_password(wrong_password, hashed_password) is False


def test_hash_password_generates_different_hashes_for_same_password():
    password = "StrongPassword123!"

    first_hash = hash_password(password)
    second_hash = hash_password(password)

    assert first_hash != second_hash
