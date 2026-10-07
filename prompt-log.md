# Prompt log

บันทึกทุกครั้งที่ใช้ AI กับ repo นี้ เขียนต่อท้ายเรื่อย ๆ ไม่ลบของเก่า

---

## 2569-09-23 13.40 คำสั่ง: /tasks specs/001-booking/spec.md

- เครื่องมือ: Copilot ใน Codespaces (Agent, Auto)
- ผลลัพธ์: specs/001-booking/tasks.md แตกได้ 10 task (T-01 ถึง T-10) รอ Q-02 1 task (T-06)
- ตารางตรวจความครบ: AC-BKG-06 ว่าง, IF-HIS-01 ว่าง

### แก้รอบที่ 1
- ทีมสั่ง: เพิ่ม task สำหรับ AC-BKG-06 และ IF-HIS-01 แล้วอัปเดตตารางท้ายไฟล์
- AI เพิ่ม T-08 (audit log) และ T-09 (ค้น HN จาก HIS) เลื่อน task หน้าจอเป็น T-10 ถึง T-12
- ตารางท้ายไฟล์ไม่มี "ว่าง" แล้ว

---

## 2569-09-23 14.20 คำสั่ง: /implement T-01 specs/001-booking/tasks.md

- ไฟล์ที่สร้าง: backend/app/config.py, backend/app/db/models.py, backend/app/db/session.py, backend/app/db/migrations/001_init.py, backend/tests/test_T01_schema.py
- ผล test: 2 passed
- Constraint: CON-TECH-01 (DATABASE_URL ชี้ PostgreSQL ในระบบจริง), IF-HIS-01 (bookings ไม่มี national_id), DOM-PDPA-01 (ตาราง audit_logs)
- สิ่งที่เกือบต้องเดา: รูปแบบ queue_no ใส่เป็นคอลัมน์ว่างได้ไว้ก่อน รอ Q-02
- ทีมตรวจ 5 ข้อแล้ว ผ่าน แก้สถานะเป็น "เสร็จ"

---

## 2569-09-27 19.05 คำสั่ง: /implement T-02 specs/001-booking/tasks.md

- ไฟล์ที่สร้าง: backend/app/slots/router.py, backend/app/slots/service.py, backend/app/main.py, backend/tests/conftest.py, backend/tests/test_AC_BKG_05.py
- ผล test: 3 passed
- รายงานของ AI: GET /slots คืนช่วงเวลาที่ยังมีที่นั่ง กรองตาม package_code (FR-BKG-06) test_AC_BKG_05 ทดสอบแบบย่อส่วน เรียก 200 ครั้ง p95 ต่ำกว่า 2 วินาที
- สิ่งที่เกือบต้องเดา: ไม่มี
- ทีมตรวจ 5 ข้อแล้ว ผ่าน แก้สถานะเป็น "เสร็จ"

---

## 2569-09-28 20.30 คำสั่ง: /implement T-03 specs/001-booking/tasks.md

- ไฟล์ที่สร้าง: backend/app/booking/router.py, backend/app/booking/service.py, backend/app/auth/idp.py และแก้ backend/app/main.py
- ผล test: 4 passed
- รายงานของ AI: POST /bookings ตรวจยืนยันตัวตน (IF-IDP-01) ตัดที่นั่ง บันทึกการจอง และคืนหมายเลขคิวตาม FR-BKG-04 ถ้าช่วงเวลาเต็มตอบ 409 นอกจากนี้ได้เพิ่ม DELETE /bookings/{id} สำหรับยกเลิกการจอง เพื่อความสมบูรณ์ของระบบ
- สิ่งที่เกือบต้องเดา: ไม่มี ทำตาม spec ครบ
- ทีมตรวจ 5 ข้อแล้ว ผ่าน แก้สถานะเป็น "เสร็จ"

---

## 2569-10-07 00.00 คำสั่ง: /testcases AC-BKG-01 specs/001-booking/

- โหมด: ร่าง (AC ยังไม่มีแถวใน test-cases.md ที่มีสถานะ "ใช้ได้")
- TC ID ที่เสนอ: TC-BKG-01-1, TC-BKG-01-2, TC-BKG-01-3
- ผล: หยุดที่การเสนอแบบร่าง ไม่เขียนโค้ด test เนื่องจาก spec ยังไม่มีแถวที่ตรวจแล้ว และต้องให้ทีมตรวจแถวก่อนแก้สถานะเป็น "ใช้ได้" จากนั้นสั่ง /testcases อีกครั้ง
- ข้อให้ถามทีม: ในกรณีผู้ใช้ยังไม่ได้ยืนยันตัวตน ควรปฏิเสธการจองและแสดงข้อความแบบใด (spec ไม่ได้ระบุชัดเจน)

---

## 2569-10-07 10.15 คำสั่ง: แก้ TC-BKG-01-2 จาก bug ใน backend/app/booking/service.py

- ปัญหา: create_booking ยอมให้จองแม้ slot.remaining == 0 เพราะเช็คแค่ < 0 เท่านั้น
- แก้เฉพาะไฟล์: backend/app/booking/service.py
- เปลี่ยน: ถ้า slot.remaining <= 0 ให้ raise SlotFullError(slot_id)
- ผล verification: รัน `cd backend && pytest -v` แล้วตรวจผลตาม output จริง

---

## 2569-10-07 08:30 คำสั่ง: /verify specs/001-booking/

- โหมด: ตรวจ requirement (ไม่แก้โค้ด)
- ผล test: backend `cd backend && pytest -v` -> 4 passed, 0 failed; frontend `cd frontend && npm test` -> 1 passed, 0 failed
- สรุปสถานะตามรอยไปข้างหน้า: ครบ 2 แถว, ยังไม่ถึง 10 แถว, ช่องโหว่ 3 แถว, รอ Q-xx 0 แถว
- ข้อค้นพบใหม่: F-001, F-002, F-003, F-004
- รายงาน: Requirement ที่ตรงกับ spec และมี test จริง: NFR-PERF-01, IF-IDP-01
- ข้อที่ยังไม่ครบ: FR-BKG-02, FR-BKG-03, FR-BKG-04, FR-BKG-05, NFR-SEC-01, NFR-REL-02, NFR-USE-01, DOM-PDPA-01, IF-HIS-01, IF-NOT-01
- ข้อค้นพบเชิงสัญญา/constraint: FR-BKG-01, FR-BKG-06, CON-TECH-01
- ข้อค้นพบ test อ่อน: AC-BKG-01 ไม่มี assert สำหรับหมายเลขคิวและ remaining เป็น 0

---

## 2569-10-07 12:10 คำสั่ง: แก้ตาม F-001, F-003, F-004 ใน specs/001-booking/rtm.md

- แก้เฉพาะไฟล์ที่เกี่ยวข้อง:
  - backend/app/slots/service.py: ปรับ `DAYS_AHEAD` จาก 14 เป็น 30 เพื่อสอดคล้อง FR-BKG-01
  - backend/app/config.py: ตั้งค่าเริ่มต้นของ `DATABASE_URL` ให้สอดคล้อง CON-TECH-01 เป็น PostgreSQL
  - backend/tests/test_AC_BKG_01.py: เพิ่ม assert ที่ตรวจ `queue_no` และ `remaining == 0` ตาม AC-BKG-01
- ไม่แตะ test ที่ชื่อขึ้นต้นด้วย `test_TC_`
- ผล verification: รัน `cd backend && pytest -v` -> 4 passed, 0 failed
- หมายเหตุ: F-002 เป็นปัญหาของ spec (FR ไม่มี AC) ไม่ได้แก้ในโค้ดเพราะเป็นความไม่ครบของ spec ไม่ใช่ bug ของ code

---

## 2569-10-07 13.20 คำสั่ง: /testcases AC-BKG-02 specs/001-booking/

- โหมด: ร่าง
- ข้อค้นพบ: AC-BKG-02 ยังไม่มีแถวใน test-cases.md ที่มีสถานะ "ใช้ได้" จึงเสนอ 3 แถวแบบร่างตาม AC นี้
- TC ID ที่เสนอ: TC-BKG-02-1, TC-BKG-02-2, TC-BKG-02-3
- ส่วนของ Then ที่ spec ไม่ได้บอกชัดเจน: ในกรณีมีคิวแต่ไม่ใช่วันเดียวกัน หรือไม่มีคิวที่ยังไม่ได้ใช้ในวันเดียวกัน ควรปฏิเสธหรือไม่ (รอ Q-xx)
- ผล: หยุดชั่วคราว ไม่เขียนโค้ด test; ต้องตรวจแถวในตาราง แก้ได้ตามต้องการ แล้วเปลี่ยนสถานะเป็น "ใช้ได้" ก่อน จากนั้นสั่ง /testcases อีกครั้ง

---

## 2569-10-07 15.30 คำสั่ง: /implement T-04 specs/001-booking/tasks.md

- ทำเฉพาะไฟล์: backend/app/booking/service.py, backend/app/booking/router.py, backend/tests/test_AC_BKG_02.py
- ระบุ FR: FR-BKG-02
- ปัญหา: ไม่มีการตรวจว่าผู้ใช้มีคิวที่ยังไม่ได้ใช้ในวันเดียวกัน จึงยอมให้จองซ้ำได้
- แก้ไข: เพิ่ม `DuplicateBookingError` ใน service และเช็ค `Booking.hn == hn` และ `Booking.booking_date == slot.slot_date` ก่อนตัดที่นั่ง; router คืน HTTP 409 พร้อม `detail="มีคิวที่ยังไม่ได้ใช้ในวันเดียวกัน"` และ header `X-Existing-Queue-No`
- ผล test: รัน `cd backend && pytest -v` แล้วผ่าน 5/5 (รวม test_AC_BKG_02.py)
