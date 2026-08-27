from __future__ import annotations

import secrets
from typing import Final

from django.core.cache import cache


class OTPService:
    """
    OTP generation, storage, verification, cooldown and rate limiting.

    Recommended cache backend:
        Redis or another shared production cache.

    Example identifier:
        email address / normalized phone number / user identifier.
    """

    PREFIX: Final[str] = "otp"

    OTP_LENGTH: Final[int] = 6
    OTP_TIMEOUT: Final[int] = 300  # 5 minutes

    MAX_VERIFY_ATTEMPTS: Final[int] = 5

    RESEND_COOLDOWN: Final[int] = 60  # 1 minute

    MAX_SEND_PER_WINDOW: Final[int] = 5
    SEND_WINDOW: Final[int] = 3600  # 1 hour

    # ------------------------------------------------------------------
    # Key helpers
    # ------------------------------------------------------------------

    @classmethod
    def _normalize_identifier(cls, identifier: str) -> str:
        """Normalize identifier before using it as a cache key."""
        return identifier.strip().lower()

    @classmethod
    def _key(cls, identifier: str) -> str:
        return f"{cls.PREFIX}:{identifier}"

    @classmethod
    def _attempt_key(cls, identifier: str) -> str:
        return f"{cls.PREFIX}:attempt:{identifier}"

    @classmethod
    def _cooldown_key(cls, identifier: str) -> str:
        return f"{cls.PREFIX}:cooldown:{identifier}"

    @classmethod
    def _send_key(cls, identifier: str) -> str:
        return f"{cls.PREFIX}:send:{identifier}"

    # ------------------------------------------------------------------
    # OTP generation
    # ------------------------------------------------------------------

    @classmethod
    def generate(cls) -> str:
        """
        Generate a cryptographically secure numeric OTP.

        Example:
            483921
        """
        minimum = 10 ** (cls.OTP_LENGTH - 1)
        maximum = 10 ** cls.OTP_LENGTH

        return str(
            secrets.randbelow(maximum - minimum) + minimum
        )

    # ------------------------------------------------------------------
    # Rate limiting
    # ------------------------------------------------------------------

    @classmethod
    def can_send(cls, identifier: str) -> bool:
        """
        Check whether the identifier has not exceeded
        the hourly OTP send limit.
        """
        identifier = cls._normalize_identifier(identifier)

        count = cache.get(cls._send_key(identifier), 0)

        return int(count) < cls.MAX_SEND_PER_WINDOW

    @classmethod
    def in_cooldown(cls, identifier: str) -> bool:
        """
        Check whether resend cooldown is active.
        """
        identifier = cls._normalize_identifier(identifier)

        return cache.get(
            cls._cooldown_key(identifier)
        ) is not None

    # ------------------------------------------------------------------
    # Save OTP
    # ------------------------------------------------------------------

    @classmethod
    def save(
        cls,
        identifier: str,
        otp: str,
        timeout: int | None = None,
    ) -> bool:
        """
        Save an OTP if rate-limit and cooldown checks pass.

        Returns:
            True  -> OTP saved successfully.
            False -> Sending is currently not allowed.
        """
        identifier = cls._normalize_identifier(identifier)

        if not identifier:
            return False

        if not otp:
            return False

        if not cls.can_send(identifier):
            return False

        if cls.in_cooldown(identifier):
            return False

        otp_timeout = (
            timeout
            if timeout is not None
            else cls.OTP_TIMEOUT
        )

        # Save OTP.
        cache.set(
            cls._key(identifier),
            otp,
            timeout=otp_timeout,
        )

        # Reset verification attempts for the new OTP.
        cache.delete(cls._attempt_key(identifier))

        # Start resend cooldown.
        cache.set(
            cls._cooldown_key(identifier),
            True,
            timeout=cls.RESEND_COOLDOWN,
        )

        # Increment hourly send counter.
        send_key = cls._send_key(identifier)

        try:
            count = cache.incr(send_key)
        except ValueError:
            # Key doesn't exist yet.
            cache.set(
                send_key,
                1,
                timeout=cls.SEND_WINDOW,
            )
        else:
            # Some cache backends may require explicit TTL handling.
            if count == 1:
                cache.set(
                    send_key,
                    count,
                    timeout=cls.SEND_WINDOW,
                )

        return True

    # ------------------------------------------------------------------
    # Verification
    # ------------------------------------------------------------------

    @classmethod
    def verify(
        cls,
        identifier: str,
        otp: str,
    ) -> bool:
        """
        Verify an OTP.

        Returns:
            True  -> OTP is valid.
            False -> OTP is invalid, expired, or attempts exceeded.
        """
        identifier = cls._normalize_identifier(identifier)

        if not identifier or not otp:
            return False

        otp = str(otp).strip()

        # Reject malformed OTP immediately.
        if len(otp) != cls.OTP_LENGTH or not otp.isdigit():
            return False

        attempt_key = cls._attempt_key(identifier)

        attempts = int(
            cache.get(attempt_key, 0)
        )

        # Maximum attempts reached.
        if attempts >= cls.MAX_VERIFY_ATTEMPTS:
            cls.delete(identifier)
            return False

        saved = cache.get(
            cls._key(identifier)
        )

        # OTP doesn't exist or has expired.
        if saved is None:
            return False

        saved = str(saved)

        # Constant-time comparison.
        if not secrets.compare_digest(saved, otp):
            try:
                new_attempts = cache.incr(attempt_key)
            except ValueError:
                cache.set(
                    attempt_key,
                    1,
                    timeout=cls.OTP_TIMEOUT,
                )
                new_attempts = 1

            # Delete OTP after the final failed attempt.
            if new_attempts >= cls.MAX_VERIFY_ATTEMPTS:
                cls.delete(identifier)

            return False

        # OTP successfully verified.
        cls.delete(identifier)

        return True

    # ------------------------------------------------------------------
    # Delete
    # ------------------------------------------------------------------

    @classmethod
    def delete(cls, identifier: str) -> None:
        """
        Delete OTP and verification-attempt state.

        Cooldown and hourly send-limit are intentionally preserved.
        """
        identifier = cls._normalize_identifier(identifier)

        cache.delete_many(
            [
                cls._key(identifier),
                cls._attempt_key(identifier),
            ]
        )