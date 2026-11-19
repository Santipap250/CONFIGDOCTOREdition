# CONFIGDOCTOR Edition — FPV Drone Workspace Implementation Plan

## เป้าหมายและข้อกำหนดการทำงาน

เปลี่ยนแอปปัจจุบันให้เป็น FPV Drone Workspace ที่หาง่าย ใช้สะดวกบนมือถือ มีโครงนำทางแบบแอปพรีเมียม และคงเครื่องมือ/API/ข้อมูลเดิมทั้งหมด งานเริ่มจาก `origin/main` SHA `f6b39ba2bada48d8c570b1784575c72abfb43521` บน branch `feature/premium-app-transformation` เท่านั้น; PR #12–#14 รวมอยู่ในฐานนี้แล้ว. ห้าม merge PR หรือ deploy Production ก่อนเจ้าของตรวจและยอมรับ Preview.

ลำดับความสำคัญคือ correctness, simplicity, stability, accessibility, speed แล้วจึงค่อย visual effects. การเปลี่ยน backend, storage, secrets หรือบริการ production ต้องมีหลักฐานและการอนุญาตแยกต่างหาก. ห้ามเปลี่ยนสูตร FPV หากไม่มีหลักฐานความผิดพลาดและ regression test. ห้ามลบ route/API/capability ที่ยังใช้งานได้.

## สถาปัตยกรรมและวิธีดำเนินงาน

1. รักษา Flask/Python 3.12, Jinja templates, static assets, 13 blueprints, database helpers, APIs และ frontend scripts ที่มีอยู่; ใช้ shared shell กับ page-scoped CSS/markup แทนการเขียนระบบใหม่. ก่อนแก้ backend ต้องมี defect ที่ทำซ้ำได้และ regression test.
2. รวมทางเข้าผู้ใช้ไว้ใน navigation ที่ชัดเจน: mobile bottom navigation มีปลายทาง Home, Tools, Analyze, Saved, More; desktop ใช้ navigation ที่มี hierarchy และไม่ซ้ำซ้อน. ทุกลิงก์ชี้ไป route ที่มีจริงหรือ state ที่ทดสอบแล้ว. ห้ามทำให้ link/API เดิมหายไปจากระบบ.
3. Tool Center ใช้ route/template ที่เข้ากับ app structure ปัจจุบัน; มีการค้นหาและกรอง รวมกลุ่ม Analyze, Tune, Build, Learn; แสดงชื่อและคำอธิบายสั้นของแต่ละ tool, empty state และ keyboard operation. กลุ่มเป็นชั้นจัดหมวด UI ไม่ใช่การลบหรือเปลี่ยน route เดิม. Saved ต้องระบุอย่างตรงไปตรงมาว่าข้อมูลอยู่ใน browser/device เท่านั้นถ้าใช้ client storage; ห้ามทำให้เข้าใจว่าซิงก์บัญชีหรือ durable cloud storage.
4. ใช้ design system ร่วม Dark Premium Futuristic: graphite/deep-navy/forest surfaces, emerald/cyan/electric-blue accents, restrained gradients/glass, consistent icons, Thai/English typography และ technical data hierarchy. รักษา brand identity ปัจจุบันและ semantics ของสีเตือน/ข้อมูล. เน้น contrast, visible focus, touch targets, forms/data readability; ใช้ micro-interactions ที่ไม่รบกวนและเคารพ `prefers-reduced-motion`.
5. ปรับ mobile-first ที่ 320/360/390/430 px, tablet และ desktop. ป้องกัน accidental horizontal overflow, overlap และ tiny controls; จัด forms/charts/tables ให้ใช้งานด้วย touch และมือเดียว; data กว้างให้เลื่อนภายใน component แทนการบีบ/ตัด. Landing video/poster ต้องมี fallback, ไม่เสียข้อมูลมือถือหรือ battery โดยไม่จำเป็น.
6. รักษา PWA install/offline behavior, manifest, SW update/cache safety และ network behavior; ห้าม cache HTML/API/session/CSRF data. เปลี่ยน cache version เฉพาะเมื่อ asset caching เปลี่ยน. คง parity ของ `static/` กับ `public/static/`.
7. ตรวจ SECURITY: `SECRET_KEY`, CSRF, secure cookie attributes, trusted proxy, input validation, security headers, rate limiter semantics, error responses และ logging. ห้ามเปิดเผย secrets. ถ้าไม่มี `DATABASE_URL` ชุมชนใช้ SQLite `/tmp` บน Vercel ซึ่งไม่ durable; ถ้าไม่มี `REDIS_URL` rate limiter เป็น per-instance memory. ห้ามอ้างว่ามี persistence หรือ shared rate limit จนได้ตั้งค่าและพิสูจน์จริง.
8. ไม่สร้างหรือเลือก paid resources, ไม่สร้าง provider resources/credentials, ไม่แก้ production secrets/services. ทางเลือก free-tier ถูกบันทึกไว้ใน `FREE_TIER_OPTIONS.md`; ทดลองได้เฉพาะเมื่อเจ้าของอนุญาต และเริ่มจาก Preview.
9. ใช้ Vercel Preview เพื่อพิสูจน์ PR deployment และ runtime ที่จำเป็น; ห้าม promote/merge/deploy Production. หากการเชื่อมต่อ Vercel หรือ external service ยังไม่ได้รับอนุญาต ให้รายงาน blocker แทนการอ้างว่า Preview สำเร็จ.

## โครงสร้างโปรเจกต์ปัจจุบันและขอบเขตการเปลี่ยน

- `app.py`, `core.py`, `blueprints/`: Flask configuration, security middleware, calculations, persistence และ route/API handlers; ตรวจและแก้เฉพาะข้อผิดพลาดที่ยืนยันได้พร้อม tests.
- `templates/base.html`, `templates/partials/`: global document shell, navigation, page headers/footer และ shared UI; เป็นจุดหลักของ information architecture.
- `templates/landing.html`, templates ของเครื่องมือ, `templates/fpv/`, error pages: คง page associations และ JavaScript hooks; ปรับ markup เฉพาะ UI ที่ต้องการ.
- `static/css/`, `static/js/`: design tokens, shared theme/responsive behavior และ interactions. จำกัด selector ให้ชัด; หลีกเลี่ยง global overrides ที่ทำลาย editor/canvas/charts/tables.
- `static/sw.js`, `static/manifest.json`, `static/video/`, `static/img/`: PWA, assets, landing media และ performance.
- `public/static/`: deployable asset mirror บน Vercel; ต้องเทียบกับ `static/` ตามข้อตกลงเดิม.
- `tests/`: pytest regression tests สำหรับ routing, APIs, security, calculations, PWA/assets, frontend source behavior; รักษาและรัน suite เดิมก่อน/หลังเปลี่ยน.
- `vercel.json`, `VERCEL_DEPLOYMENT.md`: serverless limits, environment variables, preview process และ setup documentation.
- `plan.md`, `TODO.md`, `FREE_TIER_OPTIONS.md`: implementation decisions, outcome criteria/status และ provider free-tier evidence/limitations.

## ภาษาการออกแบบ

- **Design movement:** Premium FPV instrument workspace — ความแม่นยำของเครื่องมือช่าง ผสาน editorial hierarchy ที่อ่านง่าย แทน dashboard ทั่วไปหรือ neon HUD.
- **Core principles:** (1) หาเครื่องมือได้ทันที; (2) ข้อมูลและผลวิเคราะห์อ่านง่ายก่อนความสวย; (3) responsive/accessibility เป็นส่วนหนึ่งของ UI; (4) motion และ effects ต้องไม่รบกวนการควบคุม.
- **Color philosophy:** graphite/deep-navy/forest เป็นพื้นกลางที่ลดสิ่งรบกวน; emerald/mint แสดง action/selection; cyan/electric blue ใช้กับ telemetry/links; amber/red ใช้เฉพาะสถานะเตือน/อันตราย.
- **Layout paradigm:** shared navigation แบ่งพื้นที่หลัก Home/Tools/Analyze/Saved/More; Tool Center เป็น directory ค้นหาได้; แต่ละเครื่องมือรักษา workbench/layout ที่เหมาะกับงานของตน ไม่บังคับให้ทุกหน้ากลายเป็น card grid.
- **Signature elements:** compact technical eyebrow; cards ที่แบ่งหน้าที่ด้วยเส้นขอบละเอียดและ spacing สม่ำเสมอ; active navigation/accent ที่ชัดแต่ไม่เรืองแสงเกิน.
- **Interaction philosophy:** keyboard/touch ใช้งานได้; focus/selected/loading/empty/error states ชัด; actions ไม่แสดง affordance ปลอม; Saved เปิดเผยขอบเขตการจัดเก็บ; routes/API เดิมยังเรียกได้.
- **Animation:** transitions สั้นและไม่ทำให้ layout กระโดด; ไม่มี flash, autoplay motion ที่ไม่จำเป็น หรือ animation ขัดขวาง charts; ปิด/ลด motion ตาม `prefers-reduced-motion`.
- **Typography:** คง Thai/English fonts ที่โปรเจกต์มีและทดสอบจริง; Sarabun/body สำหรับภาษาไทย, headings ชัด, monospace สำหรับ CLI/telemetry. ห้ามโหลด font/dependency ใหม่โดยไม่จำเป็น; รักษาตัวเลขและหน่วยให้อ่านง่าย.
- **Brand essence:** พื้นที่ทำงานสำหรับ FPV pilots/builders ที่ช่วยค้นหา ตรวจ และปรับ config ได้อย่างแม่นยำ — สงบ, ชัดเจน, เชื่อถือได้.
- **Brand voice:** concise, helpful, direct. ตัวอย่าง: “เลือกเครื่องมือจากงานที่ต้องทำ” และ “บันทึกไว้บนอุปกรณ์นี้ — ไม่ซิงก์ข้ามอุปกรณ์”.
- **Wordmark & logo:** รักษา CONFIGDOCTOR Edition wordmark และ assets เดิม; ไม่สร้าง identity ซ้ำหรือเปลี่ยนชื่อผลิตภัณฑ์.
- **Signature brand color:** emerald-mint เป็นสี action ที่จดจำได้ บนพื้น graphite/deep-navy; ใช้ตาม contrast/accessibility.

## Follow-up: Tool Center artwork system

- เริ่มจาก `origin/main` SHA `6fd538623542389378b431b697400b43a6c590e5` บน branch `feat/tool-card-artwork-motion`; แตะเฉพาะ Landing Tool Center และ asset mirrors.
- สร้าง icon vector และ illustration panel ที่มีความหมายเฉพาะสำหรับ tool ทั้ง 30 รายการ โดยใช้ SVG sprite แบบ same-origin เพื่อลดจำนวน request และให้ภาพคมชัดทุก viewport.
- แบ่งสีตาม Analyze/Tune/Build/Learn; ใช้ technical line art, telemetry, hardware silhouettes และ restrained glow บนกรอบ obsidian/emerald ที่มีอยู่.
- เพิ่ม motion แบบเบา (float, scan/sheen, focus/hover emphasis) เฉพาะเมื่อ `prefers-reduced-motion: no-preference`; เนื้อหาและการ์ดต้องไม่หายเมื่อ JS ใช้ไม่ได้.
- คงลิงก์, search/filter, Saved cloning, Thai/English labels, theme toggle, mobile bottom navigation และ asset parity; ไม่เพิ่ม dependency.

## ข้อจำกัดและแนวทาง rollback

ทุกการเปลี่ยนต้องแยก review ได้ใน branch/PR และสามารถ revert เป็น commit ได้. ไม่ใช้ rewrite ที่เสี่ยงสูง, ไม่เพิ่ม dependency หากทำด้วย existing stack ได้, ไม่แก้ default configuration/credentials ของ production. ยืนยัน route/API contract และ test เดิมก่อน push. Preview verification เป็นคนละขั้นกับ production publish; ไม่มี merge/promotion อัตโนมัติ.
