"""Authentication service: password hashing, sessions and account management."""
from __future__ import annotations

import hashlib
import hmac
import os
import re
import secrets
from typing import Any

from sqlmodel import Session

from ..config import settings
from ..errors import AuthenticationError, DuplicateError, ValidationError
from ..models import User
from ..repositories import (
    create_auth_session,
    create_user,
    delete_auth_session,
    find_user_by_login,
    get_user,
    get_valid_session,
    save_user,
    user_exists,
)

_ITERATIONS = 180_000
_ALGORITHM = "pbkdf2_sha256"
_USERNAME_RE = re.compile(r"^[A-Za-z0-9_.-]{3,64}$")
_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_COLORS = ["#4F46E5", "#0EA5E9", "#10B981", "#F59E0B", "#EC4899", "#8B5CF6"]


def hash_password(password: str) -> str:
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, _ITERATIONS)
    return f"{_ALGORITHM}${_ITERATIONS}${salt.hex()}${digest.hex()}"


def verify_password(password: str, stored: str) -> bool:
    try:
        algorithm, iterations, salt_hex, digest_hex = stored.split("$", 3)
        if algorithm != _ALGORITHM:
            return False
        digest = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), bytes.fromhex(salt_hex), int(iterations)
        )
        return hmac.compare_digest(digest.hex(), digest_hex)
    except (ValueError, TypeError):
        return False


def new_token() -> str:
    return secrets.token_urlsafe(32)


def _issue_token(session: Session, user_id: int) -> str:
    token = new_token()
    create_auth_session(session, user_id, token, settings.session_ttl_hours)
    return token


def register(
    session: Session,
    username: str,
    email: str,
    password: str,
    confirm: str,
    full_name: str = "",
) -> tuple[User, str]:
    username = username.strip()
    email = email.strip()
    if not _USERNAME_RE.fullmatch(username):
        raise ValidationError("Username must be 3-64 characters: letters, numbers, . _ -")
    if not _EMAIL_RE.fullmatch(email):
        raise ValidationError("Please enter a valid email address.")
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters.")
    if password != confirm:
        raise ValidationError("Passwords do not match.")
    if user_exists(session, username, email):
        raise DuplicateError("That username or email is already registered.")

    user = create_user(
        session,
        username=username,
        email=email,
        full_name=full_name.strip() or username,
        password_hash=hash_password(password),
        avatar_color=_COLORS[len(username) % len(_COLORS)],
    )
    from ..repositories import get_or_create_settings, add_activity

    get_or_create_settings(session, user.id)
    add_activity(session, user.id, "account", f"Account created for {username}")
    return user, _issue_token(session, user.id)


def login(session: Session, login_name: str, password: str) -> tuple[User, str]:
    if not login_name.strip() or not password:
        raise ValidationError("Enter both your username and password.")
    user = find_user_by_login(session, login_name)
    if user is None or not user.is_active or not verify_password(password, user.password_hash):
        raise AuthenticationError("Invalid username or password.")
    return user, _issue_token(session, user.id)


def logout(session: Session, token: str) -> None:
    if token:
        delete_auth_session(session, token)


def resolve_token(session: Session, token: str) -> User | None:
    if not token:
        return None
    auth = get_valid_session(session, token)
    if auth is None:
        return None
    return get_user(session, auth.user_id)


def update_profile(session: Session, user: User, **fields: Any) -> User:
    allowed = {"full_name", "email", "avatar_color"}
    for key, value in fields.items():
        if key in allowed and isinstance(value, str) and value.strip():
            if key == "email" and not _EMAIL_RE.fullmatch(value.strip()):
                raise ValidationError("Please enter a valid email address.")
            setattr(user, key, value.strip())
    return save_user(session, user)


def change_password(session: Session, user: User, current: str, new: str, confirm: str) -> None:
    if not verify_password(current, user.password_hash):
        raise AuthenticationError("Your current password is incorrect.")
    if len(new) < 8:
        raise ValidationError("New password must be at least 8 characters.")
    if new != confirm:
        raise ValidationError("New passwords do not match.")
    user.password_hash = hash_password(new)
    save_user(session, user)
