# รายงานภาพรวมการปรับปรุงโดเมนและ SEO — CONFIGDOCTOR Edition

**อัปเดตข้อมูล:** 20 พฤศจิกายน 2026 เวลา 00:38 UTC (07:38 น. เวลาไทย)
**Repository:** [Santipap250/CONFIGDOCTOREdition](https://github.com/Santipap250/CONFIGDOCTOREdition)
**Canonical URL เป้าหมาย:** `https://configdoctoredition.vercel.app`

## สรุปผู้บริหาร

กำหนด URL ฟรีของ Vercel ที่ต้องการให้เป็นโดเมนหลักคือ `https://configdoctoredition.vercel.app` โดยสะกดติดกัน ไม่มีขีดคั่นระหว่าง `doctor` กับ `edition` โค้ด source และเอกสารหลักถูกปรับให้ใช้ URL นี้เป็น Production fallback แล้ว และ PR #21 ถูก merge เข้า `main` จากนั้น GitHub รายงาน Vercel deployment check สำเร็จ

อย่างไรก็ตาม ณ การตรวจ HTTP สดล่าสุด หน้าเว็บยังส่ง canonical และ Open Graph URL ของโดเมนเดิม `configdoctor-edition-obixconfig.vercel.app`; `robots.txt` และทั้ง 30 URL ใน `sitemap.xml` ก็ยังอ้างโดเมนเดิมด้วย ดังนั้นการเปลี่ยน source และการ deploy สำเร็จ **ยังไม่เท่ากับ** การเปลี่ยน canonical ที่ Production เสร็จสมบูรณ์ สาเหตุที่สอดคล้องกับหลักฐานคือค่า Production `BASE_URL` ที่ถูกตั้งไว้อย่างชัดเจนยัง override ค่า fallback ใน source

## โดเมนที่ตรวจสอบ

| Host | ผลตรวจ | บทบาท/ข้อสรุป |
|---|---|---|
| `https://configdoctoredition.vercel.app` | `/` และ `/landing`, `/robots.txt`, `/sitemap.xml` ตอบ 200 | URL ฟรีที่เลือกเป็น canonical; ใช้งานได้ แต่ metadata สดยังชี้ไป host เก่า |
| `https://configdoctor-edition-obixconfig.vercel.app` | เส้นทางที่ตรวจตอบ 200 | Host เดิมของ Production; response ยังใช้เป็น canonical อยู่ |
| `https://configdoctor-edition.vercel.app` | เส้นทางที่ตรวจตอบ 404 | ชื่อที่มีขีดซึ่งเคยถูกแจ้งก่อนหน้าไม่พร้อมใช้งาน; ไม่ควรตั้งเป็น canonical |

ไม่จำเป็นต้องซื้อโดเมนเพิ่มเพื่อใช้ alias ฟรีของ Vercel ที่เลือกไว้

## โครงสร้างการสร้าง Canonical, robots และ Sitemap

- `core.py` กำหนด `_PRODUCTION_BASE_URL` เป็น `https://configdoctoredition.vercel.app`. เมื่อมี environment variable `BASE_URL` ค่า explicit นั้นมีลำดับความสำคัญสูงกว่า source fallback และถูกตัด `/` ปิดท้ายออก
- สำหรับ Vercel Preview เมื่อไม่มี `BASE_URL` โค้ดใช้ `VERCEL_URL` เพื่อให้ Preview อ้าง host ของ deployment นั้นได้; การตั้ง `BASE_URL` override ยังคงมีผลก่อน fallback ดังกล่าว
- `app.py` inject ค่า `_BASE_URL` เข้าสู่ Jinja context
- `templates/base.html` ประกอบ URL ของ Canonical และ Open Graph จาก `_BASE_URL` กับ path ของแต่ละหน้า; หน้า FPV ใช้ origin ร่วมเดียวกัน
- `blueprints/meta.py` สร้างบรรทัด `Sitemap:` ใน `/robots.txt` และ `<loc>` ทั้งหมดใน `/sitemap.xml` จาก `_BASE_URL`; sitemap มี 30 URL และ cache ภายในแอปแยกตามวันที่และ base URL
- ไม่พบไฟล์ static ที่ track ชื่อ `sitemap.xml` หรือ `robots.txt`; endpoint ทั้งคู่สร้าง response จากโค้ด
- การสแกน source/config ที่ active ไม่พบ Vercel host เก่าแบบ hard-code ใน Python, JavaScript, templates หรือ config. การอ้าง host เก่าใน BUILD_REPORT/TODO เป็นหลักฐานหรือสถานะย้อนหลังที่เก็บไว้ ไม่ใช่การตั้งค่า URL สำหรับ response ใหม่

ไม่แนะนำให้สร้าง Canonical จาก `request.host` โดยตรง เพราะ Host header อาจถูกผู้เรียกปลอมได้ แนวทางที่ปลอดภัยและตรวจสอบได้คือใช้ `BASE_URL` ที่เจ้าของกำหนด หรือค่า `VERCEL_URL` ที่แพลตฟอร์มกำหนดสำหรับ Preview

## การเปลี่ยนแปลงและประวัติ PR

1. **PR #21 — canonical hostname alignment:** เพิ่ม Production fallback `https://configdoctoredition.vercel.app`, regression assertion และปรับ README, คู่มือ Vercel, package metadata และเอกสารประกอบที่เกี่ยวข้อง PR ถูก merge เวลา 00:14:52 UTC วันที่ 20 พฤศจิกายน 2026 เป็น commit `c7d1a7b0dc4264f4955f262f256144a67a19a16d`; GitHub ได้รับ Vercel status `success` / “Deployment has completed” เวลา 00:15:07 UTC
2. **PR #22 — BUILD_REPORT update:** เพิ่มบันทึกผลตรวจหลัง merge พร้อมแยกโดเมนเป้าหมายออกจากค่าที่ response Production ยังส่งจริง PR ถูก merge เวลา 00:29:42 UTC เป็น commit `aaf449b20163905342e919b887fbcd178d88d36b`
3. ประวัติ release เก่าถูกเก็บไว้แบบมีบริบท ไม่เขียนทับข้อเท็จจริงในวันก่อนหน้า

## ผลตรวจ HTTP สด

ตรวจด้วย GET แบบไม่ล็อกอินเมื่อ 20 พฤศจิกายน 2026 เวลา 00:38:39–00:38:42 UTC:

| เส้นทางบน `configdoctoredition.vercel.app` | HTTP / Headers | เนื้อหาที่ตรวจ |
|---|---|---|
| `/` | 200; เปลี่ยนเส้นทางไป `/landing`; `Cache-Control: private, no-cache`; `Age: 0`; `X-Vercel-Cache: MISS` | Canonical และ `og:url` ยังเป็น `https://configdoctor-edition-obixconfig.vercel.app/landing` |
| `/landing` | 200; `private, no-cache`; `Age: 0`; `MISS` | Canonical และ `og:url` ยังเป็น host เก่า |
| `/robots.txt` | 200; `text/plain`; `public, max-age=86400`; `Age: 0`; `MISS` | `Sitemap:` ยังอ้าง `configdoctor-edition-obixconfig.vercel.app/sitemap.xml` |
| `/sitemap.xml` | 200; `application/xml`; `public, max-age=86400`; `Age: 0`; `MISS` | ทั้ง 30 `<loc>` ใช้ host เก่า |

การที่ `Age: 0` และ `X-Vercel-Cache: MISS` ในการตรวจนี้ไม่สนับสนุนคำอธิบายว่าเป็นเพียง Edge cache hit เก่าค้าง แต่ response ที่ตรวจยังถูกสร้าง/ส่งด้วย origin เก่าอยู่ ขณะเดียวกัน Production host เก่าก็ตอบ 200 ด้วย metadata ชุดเดียวกัน

## ผลทดสอบที่มีหลักฐาน

- ก่อน merge PR #21: full pytest suite **490 passed**; Python `compileall`, JavaScript syntax checks และ `git diff --check` ผ่านตามผลตรวจบน branch
- Flask test client แบบแยกโดยกำหนด `BASE_URL=https://base-url-check.example`: ตรวจ canonical ของ `/landing` และ `/fpv`, Sitemap directive ของ `robots.txt` และ `<loc>` ทั้ง 30 รายการ — **ผ่านทั้งหมด**
- ทดสอบการเลือก origin เมื่อไม่กำหนด `BASE_URL`: Production fallback ให้ `https://configdoctoredition.vercel.app`; Preview ใช้ค่า `VERCEL_URL` — **ผ่านทั้งคู่**
- การทดสอบ Flask แบบแยกต้องใช้ `SECRET_KEY` ชั่วคราวใน process สำหรับการเริ่มแอปเท่านั้น ไม่ได้บันทึกหรือเปลี่ยน secret บน Vercel
- ใน runtime สำหรับการตรวจครั้งล่าสุดไม่มี Python module `pytest` จึงไม่ได้รัน full suite ซ้ำในรอบจัดทำรายงานนี้

## สถานะค้างและขั้นตอนปิดงาน

Vercel authorization status ที่ตรวจเวลา 07:38 น. เวลาไทยเป็น `unauthenticated` และไม่มี stored token จึงยังไม่ได้อ่านหรือเขียนค่า Production Environment Variable ซ้ำหลังการ merge หลักฐาน Vercel ที่อ่านได้ก่อนหน้านี้ระบุ `BASE_URL` Production เป็น `https://configdoctor-edition-obixconfig.vercel.app`; การอ่านครั้งล่าสุดของ environment variable เองยังยืนยันไม่ได้เพราะไม่มีการเชื่อมต่อ แต่ผล HTTP สดยังส่ง host เก่าอยู่

เพื่อให้การเปลี่ยน canonical เสร็จจริง ต้องทำตามลำดับนี้:

1. ยืนยันตัวตน Vercel ผ่านการ์ดที่ระบบแสดง และกลับมาพิมพ์ `continue`
2. ตั้ง **Production** `BASE_URL` เป็น `https://configdoctoredition.vercel.app` โดยไม่ใส่ slash ปิดท้าย
3. สร้าง Production deployment ใหม่ตามที่เจ้าของอนุมัติไว้
4. ตรวจ response จริงซ้ำ: canonical และ `og:url` ของ `/landing`; `Sitemap:` ใน `/robots.txt`; และ host ของ `<loc>` ทั้ง 30 รายการใน `/sitemap.xml`
5. ปิดงานเมื่อทุก URL ใช้ host ใหม่และ HTTP status/headers ตอบปกติเท่านั้น

ถึงเวลาจัดทำรายงานนี้ ยังไม่มีการซื้อโดเมน ไม่มีการแก้ Production Environment Variable โดยผู้ช่วย และไม่มีการ deploy เพิ่มหลังการตรวจล่าสุด
