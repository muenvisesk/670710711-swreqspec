"""Application settings for the booking feature.

Supports: CON-TECH-01
"""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./booking.db")


settings = Settings()
