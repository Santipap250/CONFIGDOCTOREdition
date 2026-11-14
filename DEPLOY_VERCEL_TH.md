# คู่มืออัปโหลด OBIXCONFIGDOCTOR ขึ้น GitHub และเชื่อม Vercel

คู่มือนี้ใช้กับ ZIP ชุด `OBIXCONFIGDOCTOR_Vercel_Ready` โดยไม่ต้องสร้างโปรเจกต์ใหม่

## 1) เตรียมไฟล์และอัปโหลดขึ้น GitHub

1. ดาวน์โหลดและแตก ZIP บนคอมพิวเตอร์
2. เปิดโฟลเดอร์ `OBIXCONFIGDOCTOR`
3. อัปโหลด **ไฟล์และโฟลเดอร์ทั้งหมดที่อยู่ภายในโฟลเดอร์นี้** ไปไว้ที่ root ของ Repository เดียวกันกับ `app.py`, `requirements.txt` และ `vercel.json`
4. ตรวจว่าไฟล์ `app.py`, `requirements.txt`, `vercel.json`, `.python-version`, `public/`, `templates/` และ `static/` อยู่ระดับเดียวกัน ไม่ได้ซ้อนอยู่ในโฟลเดอร์ `OBIXCONFIGDOCTOR/OBIXCONFIGDOCTOR/`
5. ห้ามอัปโหลด `.env` หรือฐานข้อมูลจริงขึ้น GitHub; ใช้ `.env.example` เป็นตัวอย่างเท่านั้น

## 2) เชื่อม GitHub กับ Vercel

1. เข้า Vercel แล้วเลือก **Add New → Project**
2. Import Repository ที่เพิ่งอัปโหลด
3. ตั้ง **Root Directory** เป็น `/`
4. ปล่อย Framework/Build Command/Output Directory ให้ Vercel ตรวจจับ Flask อัตโนมัติ
5. ไม่ต้องเพิ่ม `api/index.py` และไม่ต้องใช้ `builds` หรือ catch-all `routes` แบบเก่าใน `vercel.json`

ตัวแอปเปิดเผย Flask WSGI object ชื่อ `app` ที่ไฟล์ root `app.py` ตามรูปแบบที่ Vercel ตรวจจับได้

## 3) ตั้ง Environment Variables ก่อน Deploy

เพิ่มตัวแปรต่อไปนี้ใน Vercel Project Settings → Environment Variables โดยเลือกทั้ง Preview และ Production ตามการใช้งาน

| ตัวแปร | ค่า |
|---|---|
| `SECRET_KEY` | สร้างค่าสุ่มใหม่ด้วยคำสั่ง `python -c "import secrets; print(secrets.token_hex(32))"` |
| `FLASK_DEBUG` | `0` |
| `TRUST_PROXY` | `1` |
| `FORCE_INSECURE` | `0` |
| `BASE_URL` | URL หลักของ Production เช่น `https://ชื่อโปรเจกต์.vercel.app` |
| `DATABASE_URL` | URL ของ Managed PostgreSQL ที่เปิด SSL — แนะนำให้ตั้งเพื่อเก็บ Ratings/Likes แบบถาวร |
| `REDIS_URL` | ใส่ URL ของ Redis หากต้องการ Rate Limit แบบแชร์ร่วมกันระหว่างหลาย Function instances (ไม่บังคับ) |

**ข้อสำคัญ:** อย่าใช้ค่า `SECRET_KEY` ตัวอย่างหรือส่งค่านี้ให้ผู้อื่น และอย่า commit secret ลง GitHub

ถ้ายังไม่ตั้ง `DATABASE_URL` ระบบจะ fallback ไป SQLite ใน `/tmp` เพื่อไม่ให้เกิด read-only filesystem error แต่ Ratings/Likes จะเป็นข้อมูลชั่วคราว ไม่รับประกันว่าจะคงอยู่หลังเปลี่ยน instance หรือ redeploy

## 4) Deploy Preview และตรวจสอบ

Deploy เป็น Preview ก่อน แล้วเปิด URL Preview ทดสอบเส้นทางเหล่านี้:

```text
/healthz
/landing
/app
/rates-visualizer
/team
/about
/downloads
/blackbox
/osd
/sitemap.xml
/robots.txt
/static/css/landing-premium.css
/static/img/configdoctor-logo.png
/static/img/support-qr.png
```

สิ่งที่ควรตรวจ:

- `/healthz` ตอบ JSON `{"status":"ok"}`
- หน้าเว็บไม่มี 404/500 และ CSS/โลโก้/รูป QR โหลดได้
- ทดลองส่งข้อมูลวิเคราะห์โดรนและตรวจผลลัพธ์
- ทดลอง Rates Visualizer, CLI tools และ Blackbox ด้วยไฟล์ขนาดเล็ก
- ทดลอง Export จาก OSD
- ตรวจ Vercel Runtime Logs ว่าไม่มี Import Error, Template Error หรือ Database Error

เมื่อ Preview ผ่านแล้วจึงค่อย Promote/Deploy เป็น Production

## 5) ข้อจำกัดที่ต้องทราบก่อนเปิดให้คนทั่วไปใช้

- Vercel Function จำกัด request body ที่ 4.5 MB; โปรเจกต์ตั้ง upload limit ฝั่งแอปไว้ 4 MB เพื่อเผื่อ multipart overhead ดังนั้น Blackbox CSV ขนาดใหญ่กว่านี้ต้องลดขนาดหรือใช้ direct object storage/โฮสต์ที่รองรับ upload ใหญ่กว่า
- ตั้ง Function `maxDuration` ไว้ 60 วินาทีเพื่อให้เข้ากันได้กับ Hobby plan
- Vercel Function ใช้ filesystem แบบชั่วคราว; `/tmp` ใช้เก็บไฟล์ชั่วคราวเท่านั้น ไม่ใช่พื้นที่เก็บข้อมูลถาวร
- OSD client-side export/download เป็นเส้นทางที่เหมาะกว่าไฟล์ที่บันทึกฝั่ง server ลง `/tmp`
- เพื่อให้ Community Ratings/Likes คงอยู่และแชร์ทุก instance ต้องตั้ง `DATABASE_URL` เป็น Managed PostgreSQL
- เพื่อให้ Rate Limit ทำงานสม่ำเสมอเมื่อมีหลาย instances ให้ตั้ง `REDIS_URL`

## 6) รันในเครื่องสำหรับตรวจสอบ

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

คัดลอก `.env.example` เป็น `.env`, สร้าง `SECRET_KEY` ด้วยคำสั่งข้างต้นแล้วใส่ลงใน `.env` จากนั้นรัน:

```bash
python app.py
```

เปิด `http://127.0.0.1:10000/landing`
