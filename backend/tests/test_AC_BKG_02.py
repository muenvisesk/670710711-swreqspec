# test ของ T-04: กันจองซ้ำวันเดียวกัน
# AC-BKG-02 (FR-BKG-02)
from tests.conftest import AUTH


def test_AC_BKG_02_duplicate_same_day_booking(client, db, make_slot):
    """AC-BKG-02: มีคิวที่ยังไม่ได้ใช้ในวันเดียวกัน ต้องปฏิเสธและแสดงหมายเลขคิวเดิม"""
    slot = make_slot(start="09:00", remaining=2)
    first = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)
    assert first.status_code == 201
    first_queue_no = first.json()["queue_no"]

    second = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)

    assert second.status_code == 409
    assert second.json()["detail"] == "มีคิวที่ยังไม่ได้ใช้ในวันเดียวกัน"
    assert second.headers["x-existing-queue-no"] == first_queue_no
    db.refresh(slot)
    assert slot.remaining == 1
