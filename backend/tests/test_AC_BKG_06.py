import importlib
from datetime import datetime

from sqlalchemy import create_engine, inspect

from app.db.models import AuditLog, Booking, Slot


def test_AC_BKG_06_schema_and_audit_logging():
    engine = create_engine("sqlite:///:memory:")

    # Migration creates the schema for booking and audit tables
    migration = importlib.import_module("app.db.migrations.001_init")
    migration.upgrade(engine)

    inspector = inspect(engine)
    tables = set(inspector.get_table_names())
    assert {"slots", "bookings", "audit_logs"}.issubset(tables)

    # Booking data keeps HN only and never stores national_id
    assert "hn" in Booking.__table__.columns
    assert "national_id" not in Booking.__table__.columns

    # Audit log records actor, access time and HN for patient-related access
    with engine.begin() as conn:
        conn.execute(
            Slot.__table__.insert(),
            [
                {
                    "id": 1,
                    "slot_date": "2026-09-23",
                    "start_time": "09:00",
                    "package_code": "STD",
                    "capacity": 10,
                    "remaining": 9,
                }
            ],
        )
        conn.execute(
            Booking.__table__.insert(),
            [
                {
                    "id": 1,
                    "hn": "HN-1001",
                    "slot_id": 1,
                    "booking_date": "2026-09-23",
                    "queue_no": "A001",
                    "status": "confirmed",
                    "created_at": datetime.utcnow(),
                }
            ],
        )
        conn.execute(
            AuditLog.__table__.insert(),
            [
                {
                    "id": 1,
                    "actor_id": "staff-01",
                    "action": "view_booking",
                    "hn": "HN-1001",
                    "accessed_at": datetime.utcnow(),
                }
            ],
        )

    with engine.connect() as conn:
        record = conn.execute(AuditLog.__table__.select().where(AuditLog.__table__.c.hn == "HN-1001")).first()

    assert record is not None
    assert record.actor_id == "staff-01"
    assert record.hn == "HN-1001"
