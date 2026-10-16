
# Import SQLAlchemy column types and mapping tools
from sqlalchemy import Integer, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

# Import the shared Base class from our database connection file
from src.backend.database.connection import Base


# Map this Python class to the existing MySQL "users" table
class User(Base):
    __tablename__ = "users"

    # Unique ID for each user; MySQL automatically generates it
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    # User's email address; required and must be unique
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )

    # Stores the password hash, never the plain-text password
    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    # MySQL supplies the creation timestamp by default
    created_at: Mapped[DateTime] = mapped_column(
        DateTime,
        server_default=func.current_timestamp(),
        nullable=True
    )
