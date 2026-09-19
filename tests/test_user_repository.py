from app.database.models.user import UserDB
from app.repositories.user_repository import UserRepository


def make_user(
    email: str = "test@example.com",
) -> UserDB:
    return UserDB(
        email=email,
        password_hash="hashed-password",
        is_active=True,
    )


def test_user_repository_creates_and_gets_user(db_session):
    repository = UserRepository(db_session)

    user = repository.create(
        make_user("test@example.com")
    )

    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.password_hash == "hashed-password"


def test_user_repository_gets_user_by_email(db_session):
    repository = UserRepository(db_session)

    created = repository.create(
        make_user("test@example.com")
    )

    found = repository.get_by_email("test@example.com")

    assert found is not None
    assert found.id == created.id
    assert found.email == "test@example.com"


def test_user_repository_returns_none_for_unknown_email(db_session):
    repository = UserRepository(db_session)

    found = repository.get_by_email(
        "missing@example.com"
    )

    assert found is None


def test_user_repository_gets_user_by_id(db_session):
    repository = UserRepository(db_session)

    created = repository.create(
        make_user("test@example.com")
    )

    found = repository.get_by_id(created.id)

    assert found is not None
    assert found.email == "test@example.com"