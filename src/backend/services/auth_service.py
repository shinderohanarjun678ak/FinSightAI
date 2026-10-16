# Implements registration and sign-in business logic
# Applies authentication rules and password verification

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from pwdlib import PasswordHash

from src.backend.database.models import User


# Create a password hasher using the Argon2 algorithm

password_hasher = PasswordHash.recommended()


def register_user(
    db: Session,
    email: str,
    password: str
) -> User:
   
   """
   Register a new user

   1. Check whether the email aldready exists.
   2. Hash the password.
   3. Save the user in MySQL.
   
   """

   # Remove accidental spaces and normalize the email

   email = email.strip().lower()

   # Check whether this email is aldready registered

   existing_user = (
    db.query(User)
    .filter(User.email == email)
    .first()
   )

   if existing_user:
      raise ValueError("Email is aldready registered. ")

# Never store the original password in the database

hashed_password = password_hasher.hash(password)

# Create a Python User object

new_user = User(
    email=email,
    password_hash=hashed_password
)


try:
    # Add the user to the current database transaction
    db.add(new_user)

    # Send the Insert operation to MySQL
    db.commit()

    # Load generated values, such as the user ID
    db.refresh(new_user)

    return new_user

except SQLAlchemyError:
    # Undo the transaction if a database error occurs
    db.rollback()
    raise

def authenticate_user(
    db: Session,
    email: str,
    password: str
):

  """
  Authenticate a user during sign-in.

  Return the User object if credentials are valid.
  Otherwise, return None.

  """


  # Normalize the email before searching

  email = email.strip().lower()

  # Find the account by email

  user = (
    db.query(User)
    .filter(User.email == email)
    .first()
  )

   # No account exists for this email
    if user is None:
        return None

    # Compare the entered password with the stored hash
    if not password_hasher.verify(
        password,
        user.password_hash
    ):
        return None

    # Credentials are valid
    return user
