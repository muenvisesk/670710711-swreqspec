# RTM: จองคิวตรวจสุขภาพ (Booking)
อ้างอิง: spec.md Draft v2 | tasks.md | test-cases.md
สร้างด้วย /verify เมื่อ 2569-10-07 08:30 | test: ผ่าน 5 ผ่าน 0 ไม่ผ่าน

## 1. ตามรอยไปข้างหน้า (requirement ไป โค้ด ไป test)
| ID | AC | task | โค้ด (ไฟล์: ฟังก์ชัน) | test (ผล) | สถานะ |
|---|---|---|---|---|---|
| FR-BKG-01 | AC-BKG-05 | T-02 | backend/app/slots/service.py: list_available_slots; backend/app/slots/router.py: get_slots | test_AC_BKG_05.py: PASS | ช่องโหว่ |
| FR-BKG-02 | AC-BKG-02 | T-04 | backend/app/booking/service.py: create_booking | ไม่มี test | ยังไม่ถึง |
| FR-BKG-03 | AC-BKG-03 | T-05, T-11, T-12 | backend/app/booking/router.py: create_booking; backend/app/slots/service.py: list_available_slots | ไม่มี test | ยังไม่ถึง |
| FR-BKG-04 | AC-BKG-01 | T-03, T-06 | backend/app/booking/service.py: create_booking; backend/app/booking/router.py: create_booking | test_AC_BKG_01.py: PASS (status 201 เท่านั้น) | ยังไม่ถึง |
| FR-BKG-05 | AC-BKG-04 | T-07 | ไม่มีโค้ดแจ้งคิวส่งซ้ำจริง | ไม่มี test | ยังไม่ถึง |
| FR-BKG-06 | ไม่มี AC | T-02 | backend/app/slots/router.py: get_slots; backend/app/slots/service.py: list_available_slots | ไม่มี test | ช่องโหว่ |
| NFR-PERF-01 | AC-BKG-05 | T-02 | backend/app/slots/service.py: list_available_slots | test_AC_BKG_05.py: PASS | ครบ |
| NFR-SEC-01 | ไม่มี AC | ไม่มี task | ไม่มีการตั้ง TLS/HTTPS ในโค้ด | ไม่มี test | ยังไม่ถึง |
| NFR-REL-02 | AC-BKG-04 | T-07 | ไม่มีคิวส่งซ้ำ หรือ retry หลัง 5 นาที | ไม่มี test | ยังไม่ถึง |
| NFR-USE-01 | ไม่มี AC | ไม่มี task | ไม่มีการทดสอบจริง 8/10 คน | ไม่มี test | ยังไม่ถึง |
| CON-TECH-01 | ไม่มี AC | T-01 | backend/app/config.py: DATABASE_URL; backend/app/db/session.py: engine | test_T01_schema.py: PASS (SQLite ใน test) | ช่องโหว่ |
| DOM-PDPA-01 | AC-BKG-06 | T-01, T-08 | backend/app/db/models.py: AuditLog; ไม่มี middleware บันทึกทุก request | test_T01_schema.py: PASS (ตารางมีอยู่) แต่ไม่ตรวจ audit log | ยังไม่ถึง |
| IF-IDP-01 | ไม่มี AC | T-03 | backend/app/auth/idp.py: get_verified_hn | test_AC_BKG_01.py: PASS (Authorization header) | ครบ |
| IF-HIS-01 | ไม่มี AC | T-01, T-09 | backend/app/db/models.py: Booking ไม่มี national_id; ไม่มี HIS lookup API | ไม่มี test | ยังไม่ถึง |
| IF-NOT-01 | ไม่มี AC | T-07 | ไม่มีคิวส่งข้อความ/ส่งซ้ำจริง | ไม่มี test | ยังไม่ถึง |

## 2. ตามรอยย้อนกลับ (โค้ด ไป requirement)
| โค้ด (ไฟล์: ฟังก์ชัน หรือ endpoint) | อ้าง ID | ตรงกับข้อความใน spec ไหม | หมายเหตุ |
|---|---|---|---|
| backend/app/slots/service.py: list_available_slots | FR-BKG-01, FR-BKG-06 | ไม่ตรง | เริ่มวันคำนวณด้วย 14 วัน ไม่ใช่ 30 วัน ตาม spec |
| backend/app/booking/router.py: create_booking | FR-BKG-04 | ครึ่งเดียว | เก็บ booking และตัดที่นั่งได้ แต่ยังไม่มีส่งข้อความยืนยัน/คิวส่งซ้ำ |
| backend/app/booking/service.py: create_booking | FR-BKG-02, FR-BKG-04 | ไม่ครบ | ไม่มีการป้องกันการจองซ้ำในวันเดียวกัน และยอมให้ remaining == 0 ถูกแก้เรียบร้อยแล้ว แต่ยังไม่มีการตรวจซ้ำวันเดียวกัน |
| backend/app/config.py: DATABASE_URL | CON-TECH-01 | ไม่ตรง | ค่าเริ่มต้นเป็น SQLite ใน Codespace และไม่มีการบังคับ PostgreSQL อย่างจริงจัง |
| backend/app/db/models.py: AuditLog | DOM-PDPA-01 | ไม่ครบ | มีตาราง audit_logs แต่ไม่มีการบันทึกทุก request ที่เข้าถึงข้อมูลการจอง |
| backend/app/auth/idp.py: get_verified_hn | IF-IDP-01 | ตรง | ตรวจ token ที่มีรูปแบบ Bearer verified:<HN> ก่อนให้เข้าถึง |
| backend/app/slots/router.py: get_slots | FR-BKG-01, FR-BKG-06 | ครึ่งเดียว | คืนช่วงเวลาว่างและ remaining ได้ แต่ไม่มีกลไกแสดงข้อมูลครบทุกส่วนของ spec |

## 3. ข้อค้นพบ
ชนิด: AC ไม่มี test / test อ่อน / โค้ดไม่มี FR / FR ไม่มี AC / เดา Q-xx / ละเมิด Constraint / ตัวเลขไม่ตรง spec / อ้าง ID ผิดเรื่อง
ทีมตัดสิน: แก้โค้ด / แก้ spec / เพิ่ม Q-xx / ไม่ใช่ปัญหา (พร้อมเหตุผล 1 บรรทัด)

| F-ID | ชนิด | อยู่ที่ | ขัดกับ | รายละเอียด | ทีมตัดสิน |
|---|---|---|---|---|---|
| F-001 | ตัวเลขไม่ตรง spec | backend/app/slots/service.py: list_available_slots | FR-BKG-01 | spec ระบุ 30 วันข้างหน้า แต่โค้ดใช้ DAYS_AHEAD = 14 โดยไม่มีเหตุผลจาก spec |  |
| F-002 | FR ไม่มี AC | backend/app/slots/service.py; backend/app/slots/router.py | FR-BKG-06 | FR-BKG-06 ระบุให้คำนวณช่วงว่างใหม่เมื่อเปลี่ยนแพ็กเกจ แต่ spec ไม่มี AC สำหรับเรื่องนี้ และไม่มี test ที่ตรวจจริง |  |
| F-003 | ละเมิด Constraint | backend/app/config.py: DATABASE_URL | CON-TECH-01 | ค่าเริ่มต้นเป็น SQLite://./dev.db และไม่มีการบังคับใช้ PostgreSQL ตาม constraint |  |
| F-004 | test อ่อน | backend/tests/test_AC_BKG_01.py: test_AC_BKG_01 | AC-BKG-01 | test ดึง status 201 เท่านั้น ไม่ตรวจว่า "แสดงหมายเลขคิว" และ "remaining เป็น 0" จริงตาม Then |  |

## 4. แก้แล้ว
| F-ID | แก้อย่างไร | รู้ได้อย่างไร |
|---|---|---|
| - | ไม่มี | ไม่มีข้อค้นพบเดิมที่ถูกแก้ในรอบนี้ |
