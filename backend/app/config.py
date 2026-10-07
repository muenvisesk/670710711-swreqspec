# อ่านค่าตั้งระบบจากตัวแปรสภาพแวดล้อม (CON-TECH-01)
import os

# ระบบจริงตั้ง DATABASE_URL เป็น PostgreSQL ตาม CON-TECH-01
# เช่น postgresql+psycopg://user:pass@db:5432/checkup
# ค่าเริ่มต้นควรใช้ PostgreSQL เพื่อสอดคล้องกับ constraint
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:postgres@localhost:5432/checkup",
)
