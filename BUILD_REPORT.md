# รายงานตรวจ ปรับปรุง และปล่อย OBIXCONFIGDOCTOR

## สถานะ Release

PR #2 (`fix/project-quality-pwa-accessibility`) ถูก merge เข้า `main` โดยบัญชี GitHub `Santipap250` เมื่อ 2026-11-14 18:43:26 UTC. Merge commit คือ `fe0aecedfe4410c7d1c18c146b76f7395616d111`; GitHub แสดง Vercel commit check เป็น `success` และ `Deployment has completed`. Production URL ที่ตรวจพบว่าใช้งานได้คือ [configdoctor-edition-obixconfig.vercel.app](https://configdoctor-edition-obixconfig.vercel.app). URL `configdoctor-edition.vercel.app` ไม่ได้ผูกกับ deployment นี้และตอบ 404.

## งานที่ทำ

- ปรับ validation ของตัวเลขให้ปฏิเสธ `NaN`/`Infinity`, ใช้จำนวนเซลล์แบตเตอรี่ในการเลือก PID/filter baseline และเพิ่มการ escape/จำกัดข้อมูลที่ส่งออกเป็น OSD CLI
- ปรับ navigation, PID symptom controls, Leaderboard dialogs/filters และ async loading feedback ให้รองรับ keyboard, ARIA state และ focus restoration ได้ดีขึ้น
- ปรับ Manifest ให้มีไอคอน PNG 192×192 และ 512×512 รวมถึง maskable icon เพิ่ม Service Worker offline navigation fallback ซึ่งไม่แคช HTML/API ที่อาจมีข้อมูล session และเพิ่ม root favicon route
- ปรับ `vercel.json` ให้ Flask Function เก็บ `favicon.ico` ขนาดเล็กไว้ใช้กับ root route ขณะที่ไฟล์ `favicon.png` ส่งผ่าน public static mirror; `excludeFiles` ยาว 244 ตัวอักษร
- ซิงก์ไฟล์ `static/` กับ `public/static/` ครบ 48 ไฟล์แบบ byte-identical
- ลบ template `affiliate_card.html` ที่ไม่มี caller เปลี่ยนชื่อ product catalog/package เป็น `fpv_gear_products.json`/`gear/`; คงคำแนะนำ compatibility ไว้ แต่ไม่มี PromptPay หรือ purchase/affiliate/referral URL ใน catalog/UI ที่ตรวจ
- ลบ ignore rules ซ้ำใน `.gitignore` และแก้ README/deployment guides ที่อ้าง QR asset ซึ่งไม่มีใน release

## ผลทดสอบใน Sandbox

- `python3 -m compileall -q .` — ผ่าน
- Full pytest suite — **356 passed**
- Jinja — **43 templates compiled**, ไม่มีข้อผิดพลาด
- Flask test client — landing, analyzer, PID Advisor, Leaderboard, downloads, loop analyzer, gear guide, Manifest, Service Worker และ favicon ตอบ `200`
- Chromium ที่ viewport มือถือ 390×844 และแท็บเล็ต 800×844 — ทดสอบ navigation, keyboard/focus, PID symptoms, Leaderboard dialogs และ offline fallback; ไม่พบ JavaScript page errors และหน้า Leaderboard ไม่มี horizontal overflow ที่ 390 px
- ตรวจ static mirror — 48 ไฟล์ตรงกันทุกไบต์; ตรวจ Git tracking ไม่พบ `.env`, private key หรือ SQLite database ที่ถูก track

## ผลทดสอบ Preview และ Production

- Vercel Preview ของ PR #2 แสดงสถานะ **Ready**; GitHub checks ของ Vercel ผ่านทั้ง 2 รายการ
- Preview ถูกป้องกันด้วย Vercel Authentication ตามการตั้งค่า; เมื่อเข้าผ่าน browser session ที่ยืนยันตัวตน หน้า landing, analyzer, PID Advisor, Leaderboard, downloads, loop analyzer และ gear guide ตอบ `200`
- Production route smoke test แบบไม่ใช้ login: `/`, `/landing`, `/app`, `/pid-advisor`, `/leaderboard`, `/downloads`, `/loop-analyzer`, `/fpv-gear`, `/healthz`, `/manifest.json`, `/sw.js`, `/favicon.ico`, offline page และ PWA icons ตอบ `200` ด้วย content type ที่ถูกต้อง; `/healthz` คืน `{"status":"ok"}`
- Production Manifest มี `start_url=/landing`, `scope=/`, `display=standalone`; icons 192×192, 512×512 และ maskable 512×512 โหลดได้ครบ
- Production Service Worker เป็น `obixconfigdoctor-v7-static`, สถานะ `activated` และควบคุมหน้า; Cache Storage มี 10 entries รวม offline fallback, manifest และ maskable icon
- การตรวจ PWA เป็นการตรวจ manifest/worker/assets และ browser runtime ไม่ได้อ้าง Lighthouse score หรือ certification

## Environment และข้อจำกัดที่เหลือ

Vercel Production มี environment variable ชื่อ `SECRET_KEY` และ `TRUST_PROXY` ตามการตั้งค่าก่อนหน้า โดยไม่แสดงค่าลับ ส่วน `DATABASE_URL` และ `REDIS_URL` ไม่ได้ตั้งค่าในงานนี้ จึงยังไม่มีการยืนยันความคงทนของข้อมูล Community/API บน filesystem ของ Vercel; หากต้องเก็บข้อมูลถาวร ต้องมีฐานข้อมูลภายนอกที่เจ้าของระบบตั้งค่า

ไม่มีการสร้างหรือแก้ฐานข้อมูลภายนอก ไม่มีการเปลี่ยน DNS และไม่มีการซื้อบริการหรืออัปเกรดแผนในการดำเนินงานนี้


## Addendum: canonical hostname status — 2026-11-20

The release observations above describe the Production state on 2026-11-14 and remain historical. On 2026-11-20, the alias `https://configdoctoredition.vercel.app` was attached to the READY Production deployment; the pre-existing compatibility alias remains usable, but it is not the canonical hostname. Read-only responses confirmed `/landing` (200) and the fingerprinted background video (206); the video returned `Cache-Control: public, max-age=31536000, immutable` and `X-Vercel-Cache: HIT`. However, the explicit Vercel Production `BASE_URL` is still `https://configdoctor-edition-obixconfig.vercel.app`, and live `/landing`, `/robots.txt`, and `/sitemap.xml` therefore still emit that older hostname in canonical/Open Graph/sitemap metadata. The source default, guides, repository metadata, and regression test have been aligned on branch `fix/canonical-domain-configdoctoredition`; Production environment settings, merge, and redeploy are intentionally held until the owner reviews and approves the Preview. Branch verification: 490 pytest tests passed; Python compileall, JavaScript syntax checks, and Flask test-client checks of `/landing`, `/robots.txt`, and `/sitemap.xml` passed. The Preview itself remains SSO-protected, and no share link was created.
