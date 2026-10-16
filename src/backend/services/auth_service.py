
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from pwdlib import PasswordHash

from src.backend.database.models import User

# Initialize the password hashing utility
password_hasher = PasswordHash.recommended()


def register_user(db: Session, email: str, password: str) -> User:
    """
    Register a new user.
    Store the hashed password, never the plain-text password.
    """
    email = email.strip().lower()

    # Check whether the email is already registered
    existing_user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if existing_user:
        raise ValueError("Email is already registered.")

    # Hash the password
    hashed_password = password_hasher.hash(password)

    # Create the new user
    new_user = User(
        email=email,
        password_hash=hashed_password
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user

    except SQLAlchemyError:
        db.rollback()
        raise


def authenticate_user(
    db: Session,
    email: str,
    password: str
):
    """
    Authenticate a user using email and password.
    Return the User object if valid; otherwise, return None.
    """
    email = email.strip().lower()

    # Find the user by email
    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    # Reject an unknown email
    if user is None:
        return None

    # Verify the submitted password against its hash
    if not password_hasher.verify(password, user.password_hash):
        return None

    return user
