"""
Vemetric Python SDK
"""

from __future__ import annotations

import json
import logging
from typing import Any, Dict, List, Optional, TypedDict

import requests

from ._version import __version__

_DEFAULT_HOST = "https://hub.vemetric.com"
_UA           = f"vemetric-python/{__version__}"

# Setup logger
logger = logging.getLogger("Vemetric")

class UserData(TypedDict, total=False):
    """Type for user data operations (set, setOnce, unset)."""
    set: Dict[str, Any]  # Properties to set/overwrite
    setOnce: Dict[str, Any]  # Properties to set only if not already set
    unset: List[str]  # Properties to remove

class VemetricClient:
    def __init__(
        self,
        token: str,
        host: str = _DEFAULT_HOST,
        timeout: float = 2.0,
        session: Optional[requests.Session] = None,
    ) -> None:
        if not token:
            raise ValueError("token must be provided")

        self._token   = token
        self._host    = host.rstrip("/")
        self._timeout = timeout
        self._sess    = session or requests.Session()
        self._headers = {
            "Content-Type":    "application/json",
            "User-Agent":      _UA,
            "V-SDK":           "python",
            "V-SDK-Version":   __version__,
            "Token":           token,
        }

    # ---------- Public API -------------------------------------------------

    def track_event(
        self,
        event_name: str,
        *,
        user_identifier: str,
        event_data: Optional[Dict[str, Any]] = None,
        user_data: Optional[UserData] = None,
        user_display_name: Optional[str] = None,
    ) -> None:
        if not event_name:
            raise ValueError("event_name must not be empty")
        if not user_identifier:
            raise ValueError("user_identifier must not be empty")

        payload = {
            "name": event_name,
            "userIdentifier": user_identifier,
        }
        if event_data:
            payload["customData"] = event_data
        if user_display_name:
            payload["displayName"] = user_display_name
        if user_data:
            payload["userData"] = user_data
        self._post("/e", payload)

    def update_user(
        self,
        user_identifier: str,
        *,
        user_data: Optional[UserData] = None,
    ) -> None:
        if not user_identifier:
            raise ValueError("user_identifier required")

        payload = {
            "userIdentifier": user_identifier,
        }
        if user_data:
            payload["data"] = user_data
        self._post("/u", payload)

    # ---------- Internal ----------------------------------------------------

    def _post(self, path: str, payload: Dict[str, Any]) -> None:
        url = f"{self._host}{path}"
        # remove None values to keep body compact
        filtered = {k: v for k, v in payload.items() if v is not None}

        try:
            res = self._sess.post(
                url, data=json.dumps(filtered).encode(), headers=self._headers,
                timeout=self._timeout
            )
        except requests.RequestException as exc:
            logger.error(f"Vemetric: Network error while posting to {url}: {exc}")
            return

        if res.status_code >= 300:
            logger.error(f"Vemetric: HTTP error {res.status_code} while posting to {url}: {res.text}")
            return