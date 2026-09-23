"""Initial database migration for booking data.

Supports: CON-TECH-01, DOM-PDPA-01, IF-HIS-01
"""

from __future__ import annotations

from sqlalchemy import Engine

from app.db.models import Base


def upgrade(engine: Engine) -> None:
    Base.metadata.create_all(bind=engine)
