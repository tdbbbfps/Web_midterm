from argon2 import PasswordHasher
from argon2 import exceptions
import re
from sqlalchemy.orm import Session
from . import models, schemas

# Provide password hashing, verifying and strength check.

def hash_password(password : str) -> str:
    """Hash the password and return the hashed password."""
    ph = PasswordHasher(time_cost=2, memory_cost=19456, parallelism=1, salt_len=32)
    hashed_password = ph.hash(password)
    return hashed_password

def verify_password(password : str, hashed_password : str) -> bool:
    """Verify the password against the hashed password."""
    ph = PasswordHasher()
    try:
        ph.verify(hashed_password, password)
        return True
    except exceptions.VerifyMismatchError:
        return False

def is_password_strong(password : str) -> bool:
    """Check if the pawssword is strong."""
    rule = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}")
                        # Return a match if re full match; Otherwise return None.
    return True if rule.fullmatch(password) else False


# CRUD

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """Create new user."""
    if db.query(models.User).filter((models.User.username == user.username) | (models.User.email == user.email)).first():
        return None
    if not is_password_strong(user.password):
        return None
    hashed_password = hash_password(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_id(db: Session, user_id: int) -> models.User:
    """Get user by ID."""
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str) -> models.User:
    """Get user by username."""
    return db.query(models.User).filter(models.User.username == username).first()

def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate) -> models.User:
    """Update user's information."""
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return None

    update_data = user_update.model_dump(exclude_unset=True)
    if 'password' in update_data and update_data['password']:
        update_data['password'] = hash_password(update_data['password'])
    
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int) -> bool:
    """Delete a user by ID."""
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return False
    
    db.delete(db_user)
    db.commit()
    return True


if __name__ == "__main__":
    password = input("Please enter a password: ")
    if is_password_strong(password):
        print("Password strong.")
        hashed_password = hash_password(password)
        print(f"Hashed password: {hashed_password}")
    else:
        print("Password too weak.")