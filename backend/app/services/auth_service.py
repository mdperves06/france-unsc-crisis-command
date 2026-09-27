import hashlib
import hmac
import base64
import json
import secrets
import time
from typing import Optional
from datetime import datetime, timezone

from sqlalchemy.orm import Session
from app.models.user import User, UserRole
from app.schemas.auth import UserRegister
from app.core.config import settings


# ── Password hashing (PBKDF2-HMAC-SHA256, per-user random salt) ───
_PBKDF2_ITERATIONS = 260000
_LEGACY_SALT = b"france-unsc-salt-2026"  # Hashes created before per-user salts


def _pbkdf2(password: str, salt: bytes) -> str:
    key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, _PBKDF2_ITERATIONS)
    return base64.b64encode(key).decode()


def _hash_password(password: str) -> str:
    """Hash a password as 'pbkdf2$<salt>$<hash>' with a random salt."""
    salt = secrets.token_bytes(16)
    return f"pbkdf2${base64.b64encode(salt).decode()}${_pbkdf2(password, salt)}"


def _verify_password(plain: str, hashed: str) -> bool:
    if hashed.startswith("pbkdf2$"):
        try:
            _, salt_b64, digest = hashed.split("$", 2)
            salt = base64.b64decode(salt_b64)
        except ValueError:
            return False
        return hmac.compare_digest(_pbkdf2(plain, salt), digest)
    return hmac.compare_digest(_pbkdf2(plain, _LEGACY_SALT), hashed)


# ── Simple JWT-like token (base64 encoded, HMAC signed) ──────
def _create_token(payload: dict) -> str:
    payload["exp"] = int(time.time()) + (settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    data = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode()
    sig = hmac.new(settings.SECRET_KEY.encode(), data.encode(), hashlib.sha256).hexdigest()
    return f"{data}.{sig}"


def _decode_token(token: str) -> Optional[dict]:
    try:
        parts = token.split(".")
        if len(parts) != 2:
            return None
        data, sig = parts
        expected_sig = hmac.new(settings.SECRET_KEY.encode(), data.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(sig, expected_sig):
            return None
        payload = json.loads(base64.urlsafe_b64decode(data + "==").decode())
        if payload.get("exp", 0) < int(time.time()):
            return None
        return payload
    except Exception:
        return None


# ── Auth Service ─────────────────────────────────────────────
SELF_REGISTER_ROLES = {UserRole.STUDENT, UserRole.DELEGATE}


class AuthService:

    def register_user(self, db: Session, data: UserRegister) -> User:
        # Check if email/username already exists
        if db.query(User).filter(User.email == data.email).first():
            raise ValueError("Email already registered")
        if db.query(User).filter(User.username == data.username).first():
            raise ValueError("Username already taken")
        # Coach/admin roles are granted by an admin, never self-assigned
        if data.role not in SELF_REGISTER_ROLES:
            raise ValueError("Role cannot be self-assigned")

        user = User(
            email=data.email,
            username=data.username,
            full_name=data.full_name,
            hashed_password=_hash_password(data.password),
            role=data.role,
            country_assignment=data.country_assignment or "France",
            is_active=True,
            is_verified=True,  # Auto-verify for demo; add email flow later
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def login_user(self, db: Session, email: str, password: str) -> tuple[User, str]:
        user = db.query(User).filter(User.email == email).first()
        if not user or not _verify_password(password, user.hashed_password):
            raise ValueError("Invalid email or password")
        if not user.is_active:
            raise ValueError("Account is deactivated")

        # Update last login
        user.last_login = datetime.now(timezone.utc)
        db.commit()
        db.refresh(user)

        token = _create_token({"sub": str(user.id), "email": user.email, "role": user.role})
        return user, token

    def get_current_user(self, db: Session, token: str) -> Optional[User]:
        payload = _decode_token(token)
        if not payload:
            return None
        user = db.query(User).filter(User.id == int(payload["sub"])).first()
        return user if user and user.is_active else None

    def change_password(self, db: Session, user: User, current_password: str, new_password: str) -> bool:
        if not _verify_password(current_password, user.hashed_password):
            raise ValueError("Current password is incorrect")
        user.hashed_password = _hash_password(new_password)
        db.commit()
        return True

    def get_all_users(self, db: Session) -> list[User]:
        return db.query(User).all()

    def seed_default_admin(self, db: Session):
        """Seed a default admin user if none exists."""
        if not db.query(User).filter(User.role == UserRole.ADMIN).first():
            admin = User(
                email="admin@france-unsc.org",
                username="admin",
                full_name="System Administrator",
                hashed_password=_hash_password("admin123"),
                role=UserRole.ADMIN,
                country_assignment="France",
                is_active=True,
                is_verified=True,
            )
            db.add(admin)
            db.commit()
