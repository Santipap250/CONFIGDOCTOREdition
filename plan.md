# CONFIGDOCTOR Edition — Unified Application Design Plan

## เป้าหมาย

ทำให้ทุกหน้าที่ผู้ใช้เห็นใน Flask application เชื่อมโยงกับ CONFIGDOCTOR Edition homepage ผ่าน visual system และ shared components ชุดเดียวกัน โดยคง routes, data contracts, calculations, validation, accessibility behavior และเครื่องมือเดิมไว้ การปรับจะอยู่ใน feature branch `feature/edition-full-app-design`; ไม่ merge หรือ deploy Production โดยอัตโนมัติ

## ขอบเขตจาก source

มี 34 user-facing page templates (ไม่นับ `base.html`) ครอบคลุม 30+ tools, หน้าเนื้อหา, standalone FPV hub และหน้า error 404/429/500. Homepage คือ `templates/landing.html` และใช้ `static/css/landing-premium.css`; หน้าแอปส่วนใหญ่สืบทอด `templates/base.html`, ใช้ `templates/partials/` และ `static/css/edition-pages.css`. Asset ของเว็บไซต์มี source/public mirrors ซึ่งต้องคงความตรงกัน. Production เดิมใช้ Service Worker cache `obixconfigdoctor-v9-static` แบบ cache-first สำหรับ static assets และ network-first สำหรับหน้า navigation; design batch นี้ใช้ v10 เพื่อให้ผู้ใช้เดิมรับ CSS รุ่นใหม่.

## แนวทาง implementation

1. ใช้ homepage เป็น design source of truth: dark forest background `#08110f`, raised surfaces, mint/teal accent, Manrope headings, Sarabun body, DM Mono technical labels, restrained borders, accessible focus, quiet card depth และ mobile-first spacing.
2. ใช้ `static/css/edition-tokens.css` เป็น canonical token layer ให้ homepage และหน้าภายในใช้ค่าชุดเดียวกัน; legacy variable names เป็น compatibility aliases ใน theme layer เพื่อไม่เปลี่ยน page calculations หรือ component behavior.
3. ปรับ shared shell และ shared components (navigation, page actions/hero, content rails, cards, fields, action buttons, result panels, code/table surfaces, footer และ mobile bottom navigation) ให้มี hierarchy, spacing, typography, touch targets และ state semantics ที่สม่ำเสมอ. Mobile page bar แสดง wordmark กับหน้าปัจจุบันอย่างเข้าถึงได้.
4. ใช้ page-scoped enhancements สำหรับโครงหน้าที่แตกต่างกัน แทน global overrides ที่ทำให้ workbench, charts, wide tables, uploaders, editor หรือ interactive canvas ถูกบีบ/ซ่อน. แก้ duplicate hero/title ที่ยืนยันจาก source โดยเก็บข้อมูลและลิงก์ที่มีประโยชน์ไว้.
5. ทำงานเป็น batches ตามกลุ่มหน้า: (A) tokens/shared shell/error/standalone; (B) core analysis — Drone Analyzer, PID Advisor, Blackbox, CLI Surgeon, Rates Visualizer; (C) tuning/config tools; (D) hardware/power and VTX tools; (E) FPV/training/discovery/community/resources/content pages. Batch A เริ่มแล้ว; ทุก batch ใช้ shared theme และคง route/template association เดิม.
6. รักษา Dark/teal brand, non-commercial production UI, PWA manifest/offline behavior, accessible keyboard/focus/reduced-motion, safe-area padding และ navigation consistency. หากเปลี่ยน CSS URL/cache behavior ให้ปรับ Service Worker version และ source/public mirrors ให้ถูกต้อง.

## สิ่งที่ห้ามเปลี่ยนโดยงานออกแบบนี้

- Flask route names/paths/methods, API request/response contracts, CSRF, rate limits, validation, backend analysis logic, persistence, authentication/security configuration, environment variables, database behavior, uploads constraints, copyright/legal notices, monetization policy.
- Control IDs, form names/values, JavaScript hooks, accessible labels, chart/canvas IDs, upload selectors, clipboard/share/export/import behavior, query-string/deep-link behavior, downloadable files, CLI text/data semantics หรือ PWA offline safety.
- ห้าม cache HTML/API responses หรือข้อมูลมี CSRF/session; ห้ามนำ secrets หรือข้อมูลส่วนตัวเข้า repository.

## โครงสร้างไฟล์และความรับผิดชอบ

- `templates/base.html`: document frame, metadata, shared assets, navigation/footer, body class, PWA registration.
- `templates/partials/`: shared navigation, page hero/actions, footer, bottom navigation, Open Graph metadata.
- `templates/landing.html` + `static/css/landing-premium.css`: homepage reference and catalog.
- `templates/*.html`, `templates/fpv/index.html`: page markup and page-specific interactions; preserve business logic and existing JS hooks.
- `static/css/edition-tokens.css`: canonical Edition palette/type/spacing/radius/shadow tokens used by homepage and app pages.
- `static/css/edition-pages.css`: shared application chrome and safe compatibility bridge for legacy page selectors.
- `static/css/responsive.css`, `components.css`, per-page CSS and inline styles: retain only as needed, with explicit cascade/scope decisions.
- `static/sw.js`, `public/sw.js`, `static/css/*`, `public/static/css/*`: PWA cache version v10 and deployable asset mirrors.
- `tests/`: theme, route rendering, PWA and existing functionality regression tests.
- `blueprints/`, `core.py`, `app.py`: read-only for this visual redesign unless an independent verified UI blocker requires a user-approved change.

## Design language

- **Design movement:** premium technical instrument console, softened into a calm editorial FPV workspace rather than aggressive neon HUD.
- **Core principles:** (1) hierarchy before decoration; (2) controls and results remain immediately understandable; (3) shared surfaces feel consistent while tool-specific data visualizations remain purpose-built; (4) mobile-first clarity and accessible interaction states.
- **Color philosophy:** deep green-black backgrounds communicate focus; layered charcoal-green cards separate functional zones; mint/teal marks primary actions and active states; cyan/warm/amber/red are reserved for data meaning and status.
- **Layout paradigm:** a consistent content rail and clear page introduction lead into tool-specific workspaces; forms and outputs collapse into a deliberate single-column sequence on phones while wide workbenches keep intentional horizontal room.
- **Signature elements:** compact mono eyebrow with small mint indicator; restrained surface cards with fine green-gray borders; mint action/active treatment with a subtle, non-flashing glow.
- **Interaction philosophy:** every action preserves existing behavior, exposes hover/focus/disabled/loading/empty/error states, supports keyboard/touch, and avoids visual affordances that imply unavailable features.
- **Animation:** short low-amplitude transitions only; no layout-shifting motion; honor `prefers-reduced-motion`; do not introduce animation into charts/controls where it can impair precision.
- **Typography:** Manrope for headings/UI hierarchy, Sarabun for Thai reading/body, DM Mono for technical labels, values and code. Keep code/data legible and horizontally scrollable rather than clipped.
- **Brand essence:** CONFIGDOCTOR Edition is a precise, practical FPV configuration workspace for pilots and builders; personality: calm, technical, dependable.
- **Brand voice:** concise, helpful, direct. Examples: “เริ่มจากค่าที่คุณมี แล้วค่อยไล่ดูผลทีละส่วน” and “คำสั่งพร้อมคัดลอก — ตรวจค่าให้ตรงกับรุ่นก่อนนำไปใช้”.
- **Wordmark & logo:** preserve the existing CONFIGDOCTOR Edition mark/wordmark from the homepage; use it consistently in shared chrome, not an alternate legacy wordmark.
- **Signature brand color:** mint `#75e3b4` on forest-black `#08110f`.
