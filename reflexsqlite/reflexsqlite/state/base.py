"""Root application state: authentication and shared identity."""
from __future__ import annotations

import reflex as rx

from ..config import settings
from ..db import session_scope
from ..errors import friendly
from ..services import auth_service


def _cookie_default():
    """Keep the session token in a browser cookie when supported by Reflex."""
    cookie_type = getattr(rx, "Cookie", None)
    if cookie_type is None:
        return ""
    try:
        return cookie_type(name="df_session", max_age=settings.session_ttl_hours * 3600)
    except TypeError:
        try:
            return cookie_type("df_session")
        except Exception:
            return ""


class AuthState(rx.State):
    """Every other state inherits this one, so all pages share the identity."""

    token: str = _cookie_default()
    user_id: int = 0
    username: str = ""
    full_name: str = ""
    email: str = ""
    role: str = ""
    avatar_color: str = "#4F46E5"

    # Login form
    login_name: str = ""
    login_password: str = ""
    # Registration form
    reg_username: str = ""
    reg_email: str = ""
    reg_full_name: str = ""
    reg_password: str = ""
    reg_confirm: str = ""

    auth_error: str = ""
    auth_notice: str = ""
    auth_busy: bool = False

    @rx.var
    def is_authenticated(self) -> bool:
        return self.user_id > 0

    @rx.var
    def initials(self) -> str:
        source = self.full_name or self.username or "?"
        parts = source.split()
        return "".join(part[0] for part in parts[:2]).upper() or "?"

    @rx.var
    def display_name(self) -> str:
        return self.full_name or self.username or "Guest"

    def _apply_user(self, user, token: str) -> None:
        self.token = token
        self.user_id = int(user.id)
        self.username = user.username
        self.full_name = user.full_name
        self.email = user.email
        self.role = user.role
        self.avatar_color = user.avatar_color

    def _clear_identity(self) -> None:
        self.token = ""
        self.user_id = 0
        self.username = ""
        self.full_name = ""
        self.email = ""
        self.role = ""
        self.avatar_color = "#4F46E5"

    def _restore(self) -> bool:
        """Validate the cookie token against SQLite; returns auth status."""
        with session_scope() as session:
            user = auth_service.resolve_token(session, self.token)
        if user is None:
            self._clear_identity()
            return False
        self._apply_user(user, self.token)
        return True

    @rx.event
    def require_auth(self):
        """Page on_load guard: bounce anonymous visitors to /login."""
        if not self._restore():
            return rx.redirect("/login")

    @rx.event
    def restore(self):
        self._restore()

    @rx.event
    def sign_in(self):
        self.auth_error = ""
        self.auth_busy = True
        try:
            with session_scope() as session:
                user, token = auth_service.login(session, self.login_name, self.login_password)
            self._apply_user(user, token)
            self.login_password = ""
            self.auth_notice = f"Welcome back, {user.full_name}!"
            return rx.redirect("/dashboard")
        except Exception as exc:
            self.auth_error = friendly(exc)
        finally:
            self.auth_busy = False

    @rx.event
    def sign_up(self):
        self.auth_error = ""
        self.auth_busy = True
        try:
            with session_scope() as session:
                user, token = auth_service.register(
                    session,
                    self.reg_username,
                    self.reg_email,
                    self.reg_password,
                    self.reg_confirm,
                    self.reg_full_name,
                )
            self._apply_user(user, token)
            self.reg_password = ""
            self.reg_confirm = ""
            self.auth_notice = "Your workspace is ready."
            return rx.redirect("/dashboard")
        except Exception as exc:
            self.auth_error = friendly(exc)
        finally:
            self.auth_busy = False

    @rx.event
    def sign_out(self):
        try:
            with session_scope() as session:
                auth_service.logout(session, self.token)
        except Exception:
            pass
        self._clear_identity()
        self.auth_notice = "You have been signed out."
        return rx.redirect("/login")

    # Field setters ---------------------------------------------------------
    @rx.event
    def set_login_name(self, value: str):
        self.login_name = value

    @rx.event
    def set_login_password(self, value: str):
        self.login_password = value

    @rx.event
    def set_reg_username(self, value: str):
        self.reg_username = value

    @rx.event
    def set_reg_email(self, value: str):
        self.reg_email = value

    @rx.event
    def set_reg_full_name(self, value: str):
        self.reg_full_name = value

    @rx.event
    def set_reg_password(self, value: str):
        self.reg_password = value

    @rx.event
    def set_reg_confirm(self, value: str):
        self.reg_confirm = value

    @rx.event
    def clear_auth_error(self):
        self.auth_error = ""
