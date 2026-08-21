from __future__ import annotations

import hashlib
import secrets

from django.core.cache import cache


class TokenService:
    """
    Cache-based secure token service.

    Supported purposes:
        - email_verification
        - password_reset
        - other short-lived verification flows
    """

    # ============================================================
    # CACHE PREFIX
    # ============================================================

    PREFIX = "account:token"

    # ============================================================
    # TOKEN CONFIGURATION
    # ============================================================

    TOKEN_BYTES = 32

    EMAIL_TOKEN_EXPIRE_HOURS = 24
    RESET_TOKEN_EXPIRE_HOURS = 1

    # ============================================================
    # SECURITY
    # ============================================================

    MAX_VERIFY_ATTEMPTS = 5
    VERIFY_ATTEMPT_EXPIRE_MINUTES = 60

    # ============================================================
    # RATE LIMITING
    # ============================================================

    MAX_SEND_PER_WINDOW = 5
    SEND_WINDOW = 60 * 60

    RESEND_COOLDOWN = 60

    # ============================================================
    # PURPOSES
    # ============================================================

    EMAIL_VERIFICATION = "email_verification"
    PASSWORD_RESET = "password_reset"

    # ============================================================
    # IDENTIFIER
    # ============================================================

    @staticmethod
    def _normalize_identifier(identifier: str) -> str:
        """
        Normalize identifier before creating cache keys.
        """

        return identifier.strip().lower()

    # ============================================================
    # KEY BUILDERS
    # ============================================================

    @classmethod
    def _token_key(cls, identifier: str, purpose: str) -> str:
        return (
            f"{cls.PREFIX}:"
            f"{purpose}:"
            f"value:"
            f"{identifier}"
        )

    @classmethod
    def _attempt_key(cls, identifier: str, purpose: str) -> str:
        return (
            f"{cls.PREFIX}:"
            f"{purpose}:"
            f"attempt:"
            f"{identifier}"
        )

    @classmethod
    def _cooldown_key(cls, identifier: str, purpose: str) -> str:
        return (
            f"{cls.PREFIX}:"
            f"{purpose}:"
            f"cooldown:"
            f"{identifier}"
        )

    @classmethod
    def _send_key(cls, identifier: str, purpose: str) -> str:
        return (
            f"{cls.PREFIX}:"
            f"{purpose}:"
            f"send:"
            f"{identifier}"
        )

    # ============================================================
    # TOKEN HASH
    # ============================================================

    @staticmethod
    def _hash_token(token: str) -> str:
        """
        Hash token before storing it in cache.

        Raw token is never stored.
        """

        return hashlib.sha256(
            token.encode("utf-8")
        ).hexdigest()

    # ============================================================
    # TOKEN GENERATION
    # ============================================================

    @classmethod
    def generate(cls) -> str:
        """
        Generate cryptographically secure token.
        """

        return secrets.token_urlsafe(
            cls.TOKEN_BYTES
        )

    # ============================================================
    # ISSUE TOKEN
    # ============================================================

    @classmethod
    def issue(cls, identifier: str, purpose: str, timeout: int) -> str | None:
        """
        Generate and store a token.

        Returns:
            token -> successfully generated
            None  -> blocked by cooldown/rate limit
        """

        identifier = cls._normalize_identifier(
            identifier
        )

        # --------------------------------------------------------
        # KEYS
        # --------------------------------------------------------

        token_key = cls._token_key(
            identifier,
            purpose,
        )

        attempt_key = cls._attempt_key(
            identifier,
            purpose,
        )

        cooldown_key = cls._cooldown_key(
            identifier,
            purpose,
        )

        send_key = cls._send_key(
            identifier,
            purpose,
        )

        # --------------------------------------------------------
        # RESEND COOLDOWN
        # --------------------------------------------------------

        if cache.get(cooldown_key) is not None:
            return None

        # --------------------------------------------------------
        # SEND RATE LIMIT
        # --------------------------------------------------------

        count = cache.get(
            send_key,
            0,
        )

        if count >= cls.MAX_SEND_PER_WINDOW:
            return None

        # --------------------------------------------------------
        # GENERATE TOKEN
        # --------------------------------------------------------

        token = cls.generate()

        token_hash = cls._hash_token(
            token
        )

        # --------------------------------------------------------
        # SAVE TOKEN
        # --------------------------------------------------------

        cache.set(
            token_key,
            token_hash,
            timeout,
        )

        # --------------------------------------------------------
        # RESET FAILED ATTEMPTS
        # --------------------------------------------------------

        cache.delete(
            attempt_key
        )

        # --------------------------------------------------------
        # SET COOLDOWN
        # --------------------------------------------------------

        cache.set(
            cooldown_key,
            True,
            cls.RESEND_COOLDOWN,
        )

        # --------------------------------------------------------
        # INCREMENT SEND COUNTER
        # --------------------------------------------------------

        created = cache.add(
            send_key,
            1,
            cls.SEND_WINDOW,
        )

        if not created:
            try:
                cache.incr(send_key)

            except ValueError:
                cache.set(
                    send_key,
                    1,
                    cls.SEND_WINDOW,
                )

        return token

    # ============================================================
    # VERIFY TOKEN
    # ============================================================

    @classmethod
    def verify(cls, identifier: str, purpose: str, token: str) -> bool:
        """
        Verify token.

        Token is deleted after successful verification.

        Returns:
            True  -> valid
            False -> invalid/expired/blocked
        """

        if not token:
            return False

        identifier = cls._normalize_identifier(
            identifier
        )

        token = token.strip()

        attempt_key = cls._attempt_key(
            identifier,
            purpose,
        )

        token_key = cls._token_key(
            identifier,
            purpose,
        )

        # --------------------------------------------------------
        # FAILED ATTEMPTS
        # --------------------------------------------------------

        attempts = cache.get(
            attempt_key,
            0,
        )

        if attempts >= cls.MAX_VERIFY_ATTEMPTS:
            cls.delete(
                identifier,
                purpose,
            )

            return False

        # --------------------------------------------------------
        # GET SAVED HASH
        # --------------------------------------------------------

        saved_hash = cache.get(
            token_key
        )

        if saved_hash is None:
            return False

        # --------------------------------------------------------
        # HASH PROVIDED TOKEN
        # --------------------------------------------------------

        token_hash = cls._hash_token(
            token
        )

        # --------------------------------------------------------
        # SECURE COMPARISON
        # --------------------------------------------------------

        if not secrets.compare_digest(
            str(saved_hash),
            token_hash,
        ):
            cls._record_failed_attempt(
                identifier,
                purpose,
            )

            return False

        # --------------------------------------------------------
        # SUCCESS
        # --------------------------------------------------------

        cls.delete(
            identifier,
            purpose,
        )

        return True

    # ============================================================
    # FAILED ATTEMPTS
    # ============================================================

    @classmethod
    def _record_failed_attempt(cls, identifier: str, purpose: str) -> None:
        """
        Increment failed verification attempts.
        """

        key = cls._attempt_key(
            identifier,
            purpose,
        )

        timeout = (
            cls.VERIFY_ATTEMPT_EXPIRE_MINUTES
            * 60
        )

        created = cache.add(
            key,
            1,
            timeout,
        )

        if created:
            return

        try:
            cache.incr(key)

        except ValueError:
            cache.set(
                key,
                1,
                timeout,
            )

    # ============================================================
    # DELETE TOKEN STATE
    # ============================================================

    @classmethod
    def delete(cls, identifier: str, purpose: str, *, delete_cooldown: bool = True) -> None:
        """
        Delete token verification state.

        Send-rate-limit counter is preserved.
        """

        identifier = cls._normalize_identifier(
            identifier
        )

        keys = [
            cls._token_key(
                identifier,
                purpose,
            ),
            cls._attempt_key(
                identifier,
                purpose,
            ),
        ]

        if delete_cooldown:
            keys.append(
                cls._cooldown_key(
                    identifier,
                    purpose,
                )
            )

        cache.delete_many(keys)

    # ============================================================
    # TOKEN TIMEOUT
    # ============================================================

    @classmethod
    def email_verification_timeout(cls) -> int:
        return (
            cls.EMAIL_TOKEN_EXPIRE_HOURS * 60 * 60
        )

    @classmethod
    def password_reset_timeout(cls) -> int:
        return (
            cls.RESET_TOKEN_EXPIRE_HOURS * 60 * 60
        )