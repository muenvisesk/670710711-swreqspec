# Tasks: จองคิวตรวจสุขภาพ (Booking)
- Feature: จองคิวตรวจสุขภาพ (Booking)
- Spec ID: SPEC-BKG-001
- อ้างอิง plan.md: specs/001-booking/plan.md (plan v1)
- วันที่: 2569-09-23

## สรุป
- รวมทั้งสิ้น 12 task
- มี 1 task ที่ต้องรอ Open Question (Q-02)

## รายการ task

### T-01 สร้างโครงข้อมูล PostgreSQL และ migration เบื้องต้น
- รองรับ: CON-TECH-01, DOM-PDPA-01, IF-HIS-01
- ตรวจด้วย: AC-BKG-06
- ไฟล์ที่แตะ: backend/app/db/models.py, backend/app/db/migrations/001_init.py, backend/app/config.py
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: migration สร้างตาราง slots, bookings, audit_logs และ schema เก็บเฉพาะ hn ได้ตามข้อกำหนด
- สถานะ: พร้อมทำ

### T-02 สร้าง GET /slots และคำนวณช่วงว่างตามแพ็กเกจ
- รองรับ: FR-BKG-01, FR-BKG-06, NFR-PERF-01
- ตรวจด้วย: AC-BKG-05
- ไฟล์ที่แตะ: backend/app/slots/service.py, backend/app/slots/router.py
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: GET /slots คืนช่วงเวลาว่างภายใน 30 วันพร้อมจำนวนที่นั่งคงเหลือ และมีผลทดสอบ p95 ไม่เกิน 2 วินาทีที่ผู้ใช้พร้อมกัน 200 คน
- สถานะ: พร้อมทำ

### T-03 สร้าง POST /bookings หลักและตัดที่นั่ง
- รองรับ: FR-BKG-04, IF-IDP-01
- ตรวจด้วย: AC-BKG-01
- ไฟล์ที่แตะ: backend/app/booking/router.py, backend/app/booking/service.py
- ต้องทำหลัง: T-01, T-02
- เสร็จเมื่อ: การยืนยันคิวบันทึก booking, ตัด remaining ของช่วงที่เลือกให้เหลือ 0 และคืน queue_no placeholder กลับไปยังผู้ใช้
- สถานะ: พร้อมทำ

### T-04 ป้องกันการจองซ้ำวันเดียวกัน
- รองรับ: FR-BKG-02
- ตรวจด้วย: AC-BKG-02
- ไฟล์ที่แตะ: backend/app/booking/service.py
- ต้องทำหลัง: T-03
- เสร็จเมื่อ: เมื่อมีคิวที่ยังไม่ได้ใช้ในวันเดียวกัน ระบบคืน 409 และแสดงหมายเลขคิวเดิมโดยไม่สร้าง booking ใหม่
- สถานะ: พร้อมทำ

### T-05 เสนอ 3 ช่วงที่ว่างแทนช่วงที่เต็ม
- รองรับ: FR-BKG-03
- ตรวจด้วย: AC-BKG-03
- ไฟล์ที่แตะ: backend/app/slots/service.py, backend/app/booking/service.py
- ต้องทำหลัง: T-02, T-03
- เสร็จเมื่อ: เมื่อช่วง 09.00 น. เต็ม ระบบคืน 409 พร้อม 3 ช่วงที่ใกล้ที่สุดภายในวันเดียวกันและวันถัดไป โดยไม่เกิดการจองซ้อน
- สถานะ: พร้อมทำ

### T-06 จัดการคิวส่งข้อความและ retry
- รองรับ: FR-BKG-05, IF-NOT-01, NFR-REL-02
- ตรวจด้วย: AC-BKG-04
- ไฟล์ที่แตะ: backend/app/notify/queue.py, backend/app/booking/service.py
- ต้องทำหลัง: T-03
- เสร็จเมื่อ: ระบบบันทึก booking แม้ SMS/LINE ล้มเหลว และมีงาน retry กำหนดส่งภายใน 5 นาทีตาม ASM-03
- สถานะ: พร้อมทำ

### T-07 เพิ่ม middleware audit log สำหรับการเข้าถึงข้อมูลการจอง
- รองรับ: DOM-PDPA-01
- ตรวจด้วย: AC-BKG-06
- ไฟล์ที่แตะ: backend/app/audit/middleware.py, backend/app/db/models.py
- ต้องทำหลัง: T-01, T-03
- เสร็จเมื่อ: ทุก request ที่เข้าถึงข้อมูลการจองสร้าง audit log ที่มี actor_id, accessed_at และ hn อย่างครบถ้วน
- สถานะ: พร้อมทำ

### T-08 เชื่อมต่อ HIS lookup และเก็บเฉพาะ HN
- รองรับ: IF-HIS-01, IF-IDP-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-03
- ไฟล์ที่แตะ: backend/app/his/client.py, backend/app/auth/idp.py, backend/app/booking/service.py
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: ระบบค้น HN จาก HIS ด้วยเลขบัตรประชาชนได้ และการจองไม่เก็บเลขบัตรประชาชนในฐานข้อมูล
- สถานะ: พร้อมทำ

### T-09 สร้างหน้าเลือกแพ็กเกจและช่วงเวลา (mock API)
- รองรับ: FR-BKG-01, FR-BKG-06
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-02
- ไฟล์ที่แตะ: frontend/src/pages/SlotPicker.jsx, frontend/src/App.jsx, frontend/src/api/client.js
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: หน้าจอแสดงวันและช่วงเวลาว่างพร้อมจำนวนที่นั่งคงเหลือ และเมื่อเปลี่ยนแพ็กเกจแล้วโหลดช่วงเวลาใหม่ได้
- สถานะ: พร้อมทำ

### T-10 สร้างหน้้ายืนยันและแสดง 3 ตัวเลือกเมื่อเต็ม (mock API)
- รองรับ: FR-BKG-03
- ตรวจด้วย: AC-BKG-03
- ไฟล์ที่แตะ: frontend/src/pages/ConfirmBooking.jsx, frontend/src/App.jsx, frontend/src/api/client.js
- ต้องทำหลัง: T-09
- เสร็จเมื่อ: เมื่อ API จำลองตอบ 409 หน้าจอแสดง "ช่วงเวลาเต็ม" พร้อม 3 ตัวเลือกที่ใกล้ที่สุดตามคำขอ
- สถานะ: พร้อมทำ

### T-11 ต่อหน้าจอกับ API จริง
- รองรับ: FR-BKG-01, FR-BKG-03
- ตรวจด้วย: AC-BKG-03
- ไฟล์ที่แตะ: frontend/src/pages/SlotPicker.jsx, frontend/src/pages/ConfirmBooking.jsx, frontend/src/api/client.js
- ต้องทำหลัง: T-02, T-05, T-09, T-10
- เสร็จเมื่อ: หน้าเลือกและยืนยันใช้งาน API จริงได้ โดยไม่พึ่ง mock API อีกต่อไป
- สถานะ: พร้อมทำ

### T-12 สร้างหน้าแสดงผลการจองและระบุหมายเลขคิว
- รองรับ: FR-BKG-04, FR-BKG-05
- ตรวจด้วย: AC-BKG-01, AC-BKG-04
- ไฟล์ที่แตะ: frontend/src/pages/BookingResult.jsx, frontend/src/App.jsx
- ต้องทำหลัง: T-03, T-06, T-10
- เสร็จเมื่อ: ผู้ใช้เห็นหมายเลขคิวบนหน้าจอ แม้ข้อความยืนยันไม่สำเร็จ และ UI ยังคงแสดงผลตาม booking ที่บันทึกไว้
- สถานะ: รอ Q-02

## ตารางตรวจความครบ

### 1. AC ID | task ที่ตรวจ AC นี้
| AC ID | task ที่ตรวจ AC นี้ |
|---|---|
| AC-BKG-01 | T-03, T-12 |
| AC-BKG-02 | T-04 |
| AC-BKG-03 | T-05, T-10, T-11 |
| AC-BKG-04 | T-06, T-12 |
| AC-BKG-05 | T-02 |
| AC-BKG-06 | T-01, T-07 |

### 2. Constraint ID | task ที่ทำให้เป็นจริง
| Constraint ID | task ที่ทำให้เป็นจริง |
|---|---|
| CON-TECH-01 | T-01 |
| DOM-PDPA-01 | T-01, T-07 |
| IF-IDP-01 | T-03, T-08 |
| IF-HIS-01 | T-01, T-08 |
| IF-NOT-01 | T-06 |

## สิ่งที่ยังไม่ทำ
- Q-02 หมายเลขคิวรีเซ็ตรายวัน หรือนับต่อเนื่อง และมีรูปแบบอย่างไร (เช่น A001)? -> ถามเจ้าหน้าที่เวชระเบียน
  - รอ task: T-03, T-12
