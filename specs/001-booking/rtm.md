# RTM: จองคิวตรวจสุขภาพ (Booking)
อ้างอิง: spec.md Draft v2 | tasks.md | test-cases.md
สร้างด้วย /verify เมื่อ 2569-10-07 08:50 | test: backend 5 ผ่าน 0 ไม่ผ่าน; frontend 1 ผ่าน 0 ไม่ผ่าน

## 1. ตามรอยไปข้างหน้า (requirement ไป โค้ด ไป test)
| ID | AC | task | โค้ด (ไฟล์: ฟังก์ชัน) | test (ผล) | สถานะ |
|---|---|---|---|---|---|
| FR-BKG-01 | AC-BKG-05 | T-02 | backend/app/slots/service.py: list_available_slots; backend/app/slots/router.py: get_slots | backend/tests/test_AC_BKG_05.py: PASS | ครบ |
| FR-BKG-02 | AC-BKG-02 | T-04 | backend/app/booking/service.py: create_booking; backend/app/booking/router.py: create_booking | backend/tests/test_AC_BKG_02.py: PASS | ครบ |
| FR-BKG-03 | AC-BKG-03 | T-05, T-11, T-12 | backend/frontend/src/pages/ConfirmBooking.jsx: ConfirmBooking; backend/frontend/src/api/client.js: api.createBooking | backend/frontend/src/__tests__/AC-BKG-03.test.jsx: อ่อนและไม่ถูกเรียกจาก npm test; code ยังใช้ "เต็มแล้ว" และ 2 ตัวเลือก | ช่องโหว่ |
| FR-BKG-04 | AC-BKG-01 | T-03, T-06 | backend/app/booking/service.py: create_booking; backend/app/booking/router.py: create_booking | backend/tests/test_AC_BKG_01.py: PASS | ยังไม่ถึง |
| FR-BKG-05 | AC-BKG-04 | T-07 | ไม่มี backend/app/notify/queue.py / retry queue | ไม่มี test | ยังไม่ถึง |
| FR-BKG-06 | ไม่มี AC | T-02 | backend/app/slots/service.py: list_available_slots; backend/app/slots/router.py: get_slots | ไม่มี test | ช่องโหว่ |
| NFR-PERF-01 | AC-BKG-05 | T-02 | backend/app/slots/service.py: list_available_slots | backend/tests/test_AC_BKG_05.py: PASS | ครบ |
| NFR-SEC-01 | ไม่มี AC | ไม่มี task | ไม่มี TLS/HTTPS configuration ในโค้ด | ไม่มี test | ยังไม่ถึง |
| NFR-REL-02 | AC-BKG-04 | T-07 | ไม่มี retry queue หรือ retry logic | ไม่มี test | ยังไม่ถึง |
| NFR-USE-01 | ไม่มี AC | ไม่มี task | ไม่มี test 8/10 คน | ไม่มี test | ยังไม่ถึง |
| CON-TECH-01 | ไม่มี AC | T-01 | backend/app/config.py: DATABASE_URL; backend/app/db/session.py: engine | code ใช้ PostgreSQL ในค่าเริ่มต้น | ครบ |
| DOM-PDPA-01 | AC-BKG-06 | T-01, T-08 | backend/app/db/models.py: AuditLog; ไม่มี middleware สำหรับ log ทุก request | backend/tests/test_T01_schema.py: PASS (schema เท่านั้น) | ยังไม่ถึง |
| IF-IDP-01 | ไม่มี AC | T-03 | backend/app/auth/idp.py: get_verified_hn | backend/tests/test_AC_BKG_01.py: PASS | ครบ |
| IF-HIS-01 | ไม่มี AC | T-01, T-09 | backend/app/db/models.py: Booking; ไม่มี backend/app/his/client.py | ไม่มี test | ยังไม่ถึง |
| IF-NOT-01 | ไม่มี AC | T-07 | ไม่มี backend/app/notify/queue.py หรือ async queue | ไม่มี test | ยังไม่ถึง |

## 2. ตามรอยย้อนกลับ (โค้ด ไป requirement)
| โค้ด (ไฟล์: ฟังก์ชัน หรือ endpoint) | อ้าง ID | ตรงกับข้อความใน spec ไหม | หมายเหตุ |
|---|---|---|---|
| backend/frontend/src/pages/ConfirmBooking.jsx: ConfirmBooking | FR-BKG-03 | ไม่ตรง | alert แสดง "เต็มแล้ว" และแสดงเฉพาะ 2 ตัวเลือก ไม่ตรง Then ของ AC-BKG-03 |
| backend/frontend/src/api/client.js: api.cancelBooking | Out of scope | ไม่ตรง | มีฟังก์ชันยกเลิกการจอง แม้ spec ระบุ UC-02 อยู่ใน Out of scope |
| backend/app/booking/service.py: create_booking | FR-BKG-04 | ครึ่งเดียว | บันทึกและตัดที่นั่งได้ แต่ยังไม่ส่งคำขอส่งข้อความยืนยันตาม FR-BKG-04/FR-BKG-05 |
| backend/app/db/models.py: AuditLog | DOM-PDPA-01 | ไม่ครบ | มี schema audit_logs แต่ไม่มี middleware หรือฟังก์ชันที่บันทึกทุกการเข้าถึงข้อมูลการจอง |
| backend/app/slots/service.py: list_available_slots | FR-BKG-06 | ครึ่งเดียว | เลือก package_code คัดกรองช่วงเวลาได้ แต่ไม่มี AC ที่ตรวจความถูกต้องเฉพาะเมื่อเปลี่ยนแพ็กเกจ |

## 3. ข้อค้นพบ
ชนิด: AC ไม่มี test / test อ่อน / โค้ดไม่มี FR / FR ไม่มี AC / เดา Q-xx / ละเมิด Constraint / ตัวเลขไม่ตรง spec / อ้าง ID ผิดเรื่อง
ทีมตัดสิน: แก้โค้ด / แก้ spec / เพิ่ม Q-xx / ไม่ใช่ปัญหา (พร้อมเหตุผล 1 บรรทัด)

| F-ID | ชนิด | อยู่ที่ | ขัดกับ | รายละเอียด | ทีมตัดสิน |
|---|---|---|---|---|---|
| F-005 | ของแถม | backend/frontend/src/pages/ConfirmBooking.jsx; backend/frontend/src/api/client.js | Out of scope | มีหัวข้อยกเลิกการจองและ API DELETE /bookings/{id} แม้ spec ระบุ UC-02 ว่าอยู่ใน Out of scope |  |
| F-006 | ตัวเลขไม่ตรง spec | backend/frontend/src/pages/ConfirmBooking.jsx | FR-BKG-03 | alert ปัจจุบันคือ "เต็มแล้ว" และ `slice(0, 2)` จึงไม่ตรงกับ Then: "แจ้ง 'ช่วงเวลาเต็ม' แสดง 3 ช่วงที่ว่าง" |  |
| F-007 | test อ่อน | backend/frontend/src/__tests__/AC-BKG-03.test.jsx | AC-BKG-03 | assert ใช้ `toContain('เต็ม')` และ `> 0` แทนการตรวจข้อความเป๊ะและจำนวน 3 อย่างแน่นอน |  |
| F-008 | FR ไม่มี AC | backend/app/slots/service.py; backend/app/slots/router.py | FR-BKG-06 | spec ระบุ FR-BKG-06 แต่ไม่มี AC ว่าต้องตรวจเมื่อเปลี่ยนแพ็กเกจแล้วช่วงเวลาที่ยังว่างต้องถูกคำนวณอย่างไร |  |

## 4. แก้แล้ว
| F-ID | แก้อย่างไร | รู้ได้อย่างไร |
|---|---|---|
| F-001 | ปรับค่า 30 วันตาม FR-BKG-01 | backend/app/slots/service.py มี `DAYS_AHEAD = 30` และ backend/tests/test_AC_BKG_05.py ผ่าน |
| F-003 | ตั้งค่าเริ่มต้น `DATABASE_URL` เป็น PostgreSQL ตาม CON-TECH-01 | backend/app/config.py ใช้ `postgresql+psycopg://postgres:postgres@localhost:5432/checkup` และโค้ดตรงตาม constraint |
| F-004 | เพิ่ม assert สำหรับ `queue_no` และ `remaining == 0` ใน test_AC_BKG_01 | backend/tests/test_AC_BKG_01.py ตรวจ `data["queue_no"]` และ `slot.remaining == 0` และ pytest ผ่าน 5/5 |
