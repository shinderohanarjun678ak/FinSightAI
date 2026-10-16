
# tests/test_auth_service.py

from uuid import uuid4

from sqlalchemy import text

from src.backend.database.connection import SessionLocal
from src.backend.database.models import User
from src.backend.services.auth_service import (
    register_user,
    authenticate_user,
)


def test_auth_service():
    # Generate a unique email so we don't affect an existing account.
    email = f"auth-test-{uuid4().hex[:12]}@example.com"
    password = "TestPassword123!"

    db = SessionLocal()
    user_id = None

    try:
        # 1. Confirm that the session is connected to the correct database.
        database_name = db.execute(
            text("SELECT DATABASE()")
        ).scalar_one()

        assert database_name == "finsight", (
            f"Expected database 'finsight', got {database_name!r}"
        )
        print("PASS: Connected to finsight database")

        # 2. Register a user.
        user = register_user(db, email, password)
        user_id = user.id

        assert user.id is not None
        assert user.email == email
        assert user.password_hash != password

        print("PASS: User registered")
        print("PASS: Password is stored as a hash")

        # 3. Verify the record exists in the MySQL users table.
        saved_user = db.query(User).filter(
            User.email == email
        ).first()

        assert saved_user is not None
        assert saved_user.id == user.id

        print("PASS: User record found in MySQL")

        # 4. Sign in using the correct password.
        authenticated_user = authenticate_user(
            db, email, password
        )

        assert authenticated_user is not None
        assert authenticated_user.id == user.id

        print("PASS: Correct password accepted")

        # 5. Reject an incorrect password.
        wrong_password_user = authenticate_user(
            db, email, "WrongPassword123!"
        )

        assert wrong_password_user is None

        print("PASS: Incorrect password rejected")

        # 6. Reject duplicate registration.
        try:
            register_user(db, email, password)
        except ValueError:
            print("PASS: Duplicate email rejected")
        else:
            raise AssertionError(
                "Duplicate email registration was not rejected"
            )

    finally:
        # Remove only the temporary test account.
        # This leaves your existing users untouched.
        try:
            if user_id is not None:
                test_user = db.get(User, user_id)

                if test_user is not None:
                    db.delete(test_user)
                    db.commit()
                    print("CLEANUP: Temporary test account removed")
        except Exception:
            db.rollback()
            print(
                "WARNING: Test account cleanup failed. "
                "Check the test email in MySQL."
            )
        finally:
            db.close()


if __name__ == "__main__":
    test_auth_service()
