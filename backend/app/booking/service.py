# บันทึกการจองและตัดที่นั่ง (T-03)
# รองรับ FR-BKG-04
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.models import Booking, Slot


class SlotFullError(Exception):
    """ช่วงเวลาที่เลือกไม่มีที่นั่งเหลือแล้ว"""


class DuplicateBookingError(Exception):
    """ผู้ใช้มีคิวที่ยังไม่ได้ใช้ในวันเดียวกันแล้ว"""

    def __init__(self, queue_no: str):
        self.queue_no = queue_no


def next_queue_no(db: Session, slot_date) -> str:
    """ออกหมายเลขคิวรูปแบบ A001 เริ่มนับใหม่ทุกวัน (FR-BKG-04)"""
    count = db.scalar(
        select(func.count()).select_from(Booking).where(Booking.booking_date == slot_date)
    )
    return f"A{count + 1:03d}"


def create_booking(db: Session, hn: str, slot_id: int) -> Booking:
    """ยืนยันการจอง: ตรวจซ้ำวันเดียวกัน ตรวจที่นั่ง ตัดที่นั่ง บันทึกการจอง ออกหมายเลขคิว (FR-BKG-02, FR-BKG-04)"""
    slot = db.get(Slot, slot_id)
    if slot is None:
        raise ValueError("ไม่พบช่วงเวลา")

    existing = (
        db.query(Booking)
        .filter(Booking.hn == hn, Booking.booking_date == slot.slot_date)
        .filter(Booking.status != "CANCELLED")
        .first()
    )
    if existing is not None:
        raise DuplicateBookingError(existing.queue_no or "")

    if slot.remaining <= 0:
        raise SlotFullError(slot_id)

    slot.remaining -= 1
    booking = Booking(
        hn=hn,
        slot_id=slot.id,
        booking_date=slot.slot_date,
        queue_no=next_queue_no(db, slot.slot_date),
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


