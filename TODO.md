# FPV Drone Workspace — Outcome TODO

ฐานงานคือ `origin/main` SHA `f6b39ba2bada48d8c570b1784575c72abfb43521`; ทำงานเฉพาะบน `feature/premium-app-transformation`. PR #12–#14 ถูกรวมในฐานแล้วและต้องไม่ถูกรื้อถอน. รายการที่ยังไม่ผ่าน implementation และ verification เริ่มต้นเป็น `[ ]`; อย่าทำเครื่องหมายเสร็จจากแผนหรือ source inspection เพียงอย่างเดียว.

## 1. ตรวจครบระบบและแก้เฉพาะข้อผิดพลาดที่ยืนยันได้

- [x] ตรวจ frontend, backend, Python, JavaScript, APIs/routes, database behavior, PWA, assets, security และ calculations; ทำรายการ findings แยก P0/P1/P2 พร้อม path/evidence/impact/confidence.
- [x] ค้นหาสาเหตุที่ทำซ้ำได้ของ broken buttons/links, failed forms, route/API errors, runtime/console errors, invalid inputs, calculation defects, layout problems, slow loading, caching issues และ security weaknesses; แก้เฉพาะ defect ที่ยืนยันได้และเพิ่ม regression test.
- [x] รักษาความสามารถและข้อมูลเดิม, routes, API methods/contracts, validation, security, calculations, download/export/import, keyboard controls และ user workflows; ห้ามลบ capability หรือเปลี่ยนสูตร FPV หากไม่มีหลักฐานและ test.

## 2. โครงนำทางและ Tool Center

- [x] Mobile bottom navigation ต้องมีปลายทาง **Home, Tools, Analyze, Saved, More**; ให้เข้าถึงง่ายและรองรับ safe-area, touch, focus, keyboard, active state และ viewport 320/360/390/430 px.
- [x] Desktop navigation ต้องมี hierarchy ที่เหมาะสมและไม่ซ้ำซ้อน; ทุกปลายทางใช้ route/state ที่มีอยู่หรือพิสูจน์แล้ว; คงลิงก์ที่มีประโยชน์และเส้นทางใช้งานเดิม.
- [x] สร้าง Tool Center จุดเดียวที่ค้นหาและกรองได้; แบ่งเครื่องมือเป็น **Analyze, Tune, Build, Learn**; ค้นหา/กรองใช้ keyboard ได้, มี empty state และแต่ละรายการมีชื่อ/รายละเอียด/ลิงก์ที่ถูกต้อง.
- [x] เพิ่ม Saved destination โดยไม่สร้างข้ออ้างเรื่อง account/cloud sync; ถ้าใช้ browser storage ให้ระบุว่าเก็บเฉพาะอุปกรณ์และจัดการ storage errors/fallback; ห้ามแทนที่ persistence/API ที่มีอยู่.
- [x] ทำให้ common actions ชัดเจนและเข้าถึงได้ในไม่กี่ taps โดยไม่ลบ tool routes/API เดิม.

## 3. Design system ทุกหน้า

- [x] ใช้ Dark Premium Futuristic ร่วมกันทั้งหน้าแรกและหน้าแอป: graphite/deep-navy surfaces, emerald/cyan/electric-blue accents, restrained gradients/glass, consistent icons, Thai/English typography, polished cards และ clear chart/data presentation.
- [x] ให้ visual hierarchy, readability, contrast, forms, states และ interaction semantics คงเส้นคงวา โดยไม่เปลี่ยนความหมายสีสถานะ/ข้อมูลหรือทำให้หน้าเครื่องมือเฉพาะทางกลายเป็น generic dashboard.
- [x] มี micro-interactions และ smooth transitions เฉพาะที่ช่วยใช้จริง; ไม่มี excessive glow/motion; เคารพ `prefers-reduced-motion`.

## 4. Mobile-first, accessibility และ landing performance

- [x] ปรับทุกหน้าให้ใช้งานที่ 320, 360, 390, 430 px, tablet และ desktop; ไม่มี accidental horizontal overflow, overlapping controls หรือ tiny touch targets.
- [x] Forms, charts, tables และ navigation ต้องสะดวกบน touch/one-handed use; ข้อมูลกว้างยังอ่านครบด้วย intentional internal scrolling.
- [x] รักษา existing PWA installability/offline state; ตรวจ manifest, service worker, offline behavior, cache update และไม่ cache HTML/API/session/CSRF responses.
- [x] Optimize landing video/poster เพื่อไม่สิ้นเปลือง mobile data/battery/load time; มี poster/fallback ที่เหมาะสมและยังแสดงภาพได้เมื่อ media ไม่โหลด.

## 5. Backend, data และ security

- [x] ตรวจ `SECRET_KEY`, CSRF, cookie attributes, `TRUST_PROXY`, validation, security headers, rate limiting และ API error responses; แก้เฉพาะ weakness ที่ยืนยันได้พร้อม regression tests; ห้ามเปิดเผย secrets.
- [x] ตรวจ persistence/rate-limit behavior ใน local และ Vercel semantics; ถ้าไม่มี `DATABASE_URL`, community ratings/likes อาจใช้ SQLite ใน `/tmp` ซึ่งไม่ durable; ถ้าไม่มี `REDIS_URL`, rate limits เป็น in-memory/per-instance; อย่ารายงานว่า persistent/shared จนกว่าจะกำหนดและพิสูจน์.
- [x] ตรวจ free options และบันทึก quotas, limitations และขั้นตอน setup ที่ปลอดภัยใน `FREE_TIER_OPTIONS.md`; ห้ามสร้าง paid resources, สร้าง credentials, เปลี่ยน production secrets/services หรือเปิดเผย secrets โดยไม่มีอนุญาต.

## 6. Engineering hygiene และ compatibility

- [x] ทำงานบน `feature/premium-app-transformation`, ไม่แก้ `main`; รักษา commit/changes ของ PR #12–#14.
- [x] รักษา parity ระหว่าง `static/` และ `public/static/`; ไม่มี dependency ที่ไม่จำเป็นหรือ rewrite เสี่ยงสูง; เปลี่ยนแปลง reviewable, focused และ rollbackable.
- [x] คงการทำงานเดิมของ Flask/Python 3.12, Jinja, route/API contracts, existing forms/hooks/IDs, charts/canvas, uploads, exports และ PWA.

## 7. Verification และ handoff

- [x] รัน full existing + new pytest suite และ Python compilation; รัน route/API smoke tests และทดสอบ broken links/buttons, core user workflows, responsive viewport, performance/security checks และ static/public parity.
- [x] แยกผลจริงจากสิ่งที่รันไม่ได้; บันทึก test commands/counts/failures, environment prerequisites และ limitations; ห้ามอ้างว่าผ่านจาก HTTP 200 เพียงอย่างเดียว.
- [ ] Push branch, ส่ง PR ไป `main`, สร้างและตรวจ Vercel Preview; รายงาน audit findings P0/P1/P2, fixes, pages/tools changed, test results, responsive/performance results, setup ที่ยังต้องทำ, PR URL และ Preview URL.
- [ ] ห้าม merge PR หรือ deploy/promote Production จนกว่าเจ้าของตรวจรับ Preview และอนุมัติ.

## 8. Follow-up: Tool Center icons and artwork (branch `feat/tool-card-artwork-motion`)

- [x] เปลี่ยน glyph text ของ tool ทั้ง 30 รายการเป็น icon vector ที่แตกต่างกันและสื่อความหมายของเครื่องมือนั้น.
- [x] เพิ่ม illustration ในกรอบของการ์ดครบทั้ง 30 รายการ โดย mapping ต้อง unique, อ้างอิงเครื่องมือจริง และทำงานกับ Saved cards ที่ clone จากการ์ดต้นทาง.
- [x] เพิ่ม motion ที่โดดเด่นแต่ไม่รบกวน; เคารพ `prefers-reduced-motion`, แสดงเนื้อหาได้เมื่อ JavaScript ไม่พร้อม, และคง Theme/Language/keyboard/touch behavior เดิม.
- [x] ไม่มี dependency ใหม่โดยไม่จำเป็น; parity ของ source assets กับ `public/static/`; ทดสอบทุกการ์ด, route, filter/search/Saved และ viewport มือถือ/desktop.
- [ ] Push branch, เปิด PR และยืนยัน Vercel Preview; ห้าม merge หรือ deploy Production ก่อนเจ้าของตรวจรับและอนุมัติ.

## หลักฐานสถานะเริ่มต้น

- [x] ยืนยัน `origin/main` SHA `f6b39ba2bada48d8c570b1784575c72abfb43521`; branch ใหม่ตรงกับ main และ worktree สะอาดก่อนเริ่มแก้โค้ด.
- [x] Baseline full suite บนฐานเริ่มต้น: `SECRET_KEY=premium-audit-baseline FLASK_DEBUG=1 /tmp/configdoctor-venv/bin/python -m pytest -q` — **464 passed in 3.25s**.
- [x] อ่าน master prompt, ตรวจ repository inventory และจัดทำแผน/บันทึกผู้ให้บริการ Free tier โดยไม่ provision resources.

## หลักฐานตรวจล่าสุด

- `pytest -q`: **473 passed in 2.75s**; `compileall`, `node --check static/sw.js`, mirror parity และ `git diff --check` ผ่าน.
- Playwright ตรวจ **34 routes × 6 widths (320/360/390/430/768/1440px) = 204 renders**; ไม่พบ HTTP/overflow failures หรือ browser page errors. ทดสอบ Landing search/filter/zero-results, Saved add/remove/reload/localStorage denial, Analyzer POST workflow, Flight Quiz radio keyboard, Rates Visualizer Enter/Space, และ Service Worker offline fallback (503) ผ่าน.
- Video: `/static/video/landing-background.mp4` 5,291,031 bytes; poster 53,190 bytes. ไม่พบ request เมื่อจอเล็ก, reduced motion หรือ Save-Data; desktop ได้ HTTP 206. Local browser measurement: DOMContentLoaded 448 ms, load 669 ms; เป็นผล local ไม่ใช่ RUM/production network.
- Security test client: headers และ session flags (HttpOnly/SameSite=Lax/Secure) ผ่าน; missing-CSRF API request ยังคงถูกปฏิเสธ 400 และตอบ JSON. Rate limiter ใช้ memory เมื่อไม่มี `REDIS_URL`; ยังไม่มีหลักฐานว่ามี shared Redis ใน Vercel.
- PWA/style source กับ `public/static/` mirrors ตรงกัน. พบ/แก้ confirmed P2: cache asset เมื่อไม่มี Content-Length, API CSRF error เป็น HTML, quiz keyboard/zoom, non-native role=button ไม่มี activation, README GitHub URL เก่า, desktop Tools/More active-state ซ้ำ และ navigation rewrite ทำให้ theme/menu-language preferences เดิมหายไป. คืน `obix-theme`/`obix-lang` controls บน Landing และ desktop More; Playwright ยืนยัน toggle, reload persistence, เมนู Landing แปลได้ และ localStorage denial ไม่ทำให้ JS error. ไม่มี P0/P1 ที่ยืนยันได้ ณ ตอนนี้; production DB/Redis และ Vercel environment ไม่ได้แก้ไขหรือยืนยัน.
- Vercel MCP ยัง unauthenticated/no stored token; Preview ยังไม่ยืนยัน. PR/Preview เป็นขั้นตอนค้างจนกว่าจะ push/open PR และตรวจ GitHub/Vercel deployment status.

## ประวัติที่ต้องรักษา

- PR #12–#14 merge เข้า `main` ก่อนเริ่มงานนี้; changes และ tests เหล่านั้นอยู่ใน base SHA ข้างต้น. ห้าม cherry-pick ซ้ำหรือย้อนการแก้ไข.


## Follow-up: Landing background video resource optimization (branch `perf/landing-video-optimization`)

- [x] Keep the Landing poster as the immediate visual fallback and defer assigning/loading the background MP4 until after the initial page load and an idle opportunity, so video transfer does not compete with the critical paint/LCP window.
- [x] Reduce the MP4 file size while retaining the existing visual content, framing, and motion at an acceptable inspected quality; keep the existing reduced-motion, mobile, Save-Data, and 2G/3G no-video behavior.
- [x] Use a content-fingerprinted video URL, mirror identical bytes under `static/` and `public/static/`, and apply long-lived immutable caching only to that fingerprinted URL; preserve the poster/fallback if media cannot load or play.
- [x] Deliver the change on this branch through a GitHub PR and verify its Vercel Preview if available; do not merge or deploy/promote Production before owner acceptance.


Verification update: final pytest passed (489 tests in 2.74s); Python compileall, `node --check` for the service worker and inline Landing script, `vercel.json` parsing, `git diff --check`, stale-path scan, and static/public byte parity passed. `ffprobe` confirmed H.264 High, 720×1280, 30 fps, 26.666667 seconds, 2,706,358 bytes. Local browser QA observed the 53,490-byte poster at 66 ms and MP4 transfer beginning 1,159 ms after `loadEventEnd`; Chromium left the source unset at 390×844, under reduced motion, and on simulated 3G. No post-change LCP value was measured. PR #20's exact Vercel deployment is `READY`, but deployed HTML/video response and Cache-Control remain unverified because Preview requires SSO and no temporary share link was approved.


Handoff status: PR #20 is now merged; see the current merge and Production records below. The owner chose to keep the current Production deployment, with no rollback. The Preview remains SSO-protected, and deployed HTML/video response headers are unverified because no temporary share link was approved.


Merge record: GitHub reports PR #20 was merged by `Santipap250` at 2026-11-20 05:54:42 +07 as merge commit `d2ad28d01d7f88312cec7022c3d984d467864bde`.
Production record: Vercel deployment `dpl_CQo4fhweFycmeRybmTEWSBrMSqQX` for that commit is `READY` and carries the `configdoctor-edition-obixconfig.vercel.app` alias.
Owner decision: keep the current Production deployment; no rollback was performed. No temporary Preview share link was created, so the deployed Cache-Control response remains unverified.
