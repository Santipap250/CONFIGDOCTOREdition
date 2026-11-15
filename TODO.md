# CONFIGDOCTOR Edition — Full Application Design TODO

สถานะ: unified redesign ผ่าน PR #9 ซึ่งบัญชีเจ้าของ repository merge แล้ว; follow-up ปรับ mobile simulator (PR #10) รวมอยู่ใน main ที่ commit 9bf7bfc แล้ว — ยืนยันจากโค้ดใน `templates/fpv_trainer.html` (กฎ 56px header clearance) และ commit hash ในไฟล์ ZIP

## Canonical design system and shared shell
- [x] หน้าแรกและทุกหน้าแอปใช้ palette, typography, spacing, radii และ focus/interaction language เดียวกันกับ CONFIGDOCTOR Edition; tokens มีแหล่งอ้างอิงกลางโดยไม่ทำให้ legacy selectors เสีย.
- [x] Shared navigation, page actions, page introduction, content rail, footer และ mobile navigation ใช้แบรนด์ CONFIGDOCTOR Edition อย่างสม่ำเสมอทุก viewport; keyboard, focus, Escape/close, safe-area และ reduced-motion behavior ที่มีต้องคงอยู่.
- [x] Cards, forms, primary/secondary/danger actions, statuses, tables, charts, code/editor, upload areas, empty/loading/error states มี visual hierarchy และ responsive treatment สม่ำเสมอ โดยสีสถานะ/ข้อมูลเชิงความหมายไม่ถูกลบหรือเปลี่ยนความหมาย.
- [x] Standalone FPV hub และ 404/429/500 มี shared brand/tokens และลิงก์นำทางที่สอดคล้อง; status meaning, privacy/security messages และ copyright/legal notices คงเดิม.

## Core analysis tools
- [x] Drone Analyzer, PID Advisor, Blackbox Analyzer, CLI Surgeon และ Rates Visualizer ใช้ unified design system; forms/inputs, results, charts, code/editor, loading/empty/error states และ mobile hierarchy ชัดเจน.
- [x] รักษา API/routes/HTTP methods, query/deep links, CSRF, validation, file handling, analysis results, PID/filter recommendations, copy/share/export/import, presets, charts และ JavaScript hooks/IDs/names/ARIA behavior ตามเดิม.
- [x] หัวข้อซ้ำหรือหน้าแรกที่กินพื้นที่เกินจำเป็นแก้ได้เฉพาะ presentation โดยเก็บข้อมูลและเส้นทางใช้งานสำคัญไว้.

## Tuning and configuration tools
- [x] Quick Tune Pad, RPM Filter Calculator, Betaflight Config Wizard, CLI Comparator, Build Card Generator, Tuning Log และ OSD Designer มี shared hierarchy สำหรับ stepper/form/result/editor/export และยังอ่านข้อมูลเชิงเทคนิคได้ครบ.
- [x] รักษาค่าคอนฟิก, validation, presets, calculations, state transitions, chart/preview, copy/export/download, persistence และ keyboard/touch behavior.

## Hardware, power and RF tools
- [x] Motor × Prop Recommender, ESC Checker, Battery Health Advisor, Motor Thermal Estimator, Control Loop Analyzer, VTX Bands/Channels, VTX Range และ SmartAudio/Tramp ใช้ card/data hierarchy และ responsive rules เดียวกัน โดยรักษา visualization/table ที่ต้องใช้พื้นที่กว้าง.
- [x] รักษาสูตร, units, inputs/outputs, warnings, frequency/channel data, compatibility rules, copy/share behavior, chart/table content และข้อจำกัดความปลอดภัยเดิม.

## FPV, learning, community and content pages
- [x] FPV Training Simulator, Flight Style Quiz, Military UAS Analyzer, Leaderboard, FPV Knowledge Hub, FPV Gear Guide, Downloads, About, Team และ Changelog เชื่อมกับ shared design system และมี navigation/reading hierarchy สอดคล้องกัน.
- [x] รักษา game/quiz controls, keyboard/gamepad behavior, community votes/rate limits, list filtering, download targets, external links, content, attribution/copyright และ accessibility semantics.

## Cross-cutting release criteria
- [x] ไม่มีการเปลี่ยน backend routes/API/data/security behavior หรือสร้าง monetization, PromptPay, affiliate UI ขึ้นมาใหม่.
- [x] PWA manifest, offline fallback, safe service-worker cache policy และ static source/public mirrors ยังคงถูกต้อง; เปลี่ยน cache key เมื่อจำเป็นเพื่อเผยแพร่ asset รุ่นใหม่.
- [x] ทุก page route ที่มี UI ใช้ธีมร่วม, ไม่มี horizontal overflow ที่ไม่ตั้งใจบนมือถือ, wide data/workbench ยังคงใช้งานได้.
- [ ] manual JavaScript console/runtime-error sweep: ทำบางส่วนแล้ว (ดูหัวข้อ "Mobile / accessibility / runtime QA sweep" ด้านล่าง); ยังไม่ครอบคลุม FPV Simulator (three.js), กราฟ Chart.js, gamepad และ Leaderboard dialogs
- [x] Follow-up mobile Simulator height fix (56px header clearance) ผ่าน Vercel Preview ที่ 390×844; game area จบที่ y=843.89px และไม่มี horizontal overflow. PR #10 merge เข้า main แล้ว (รวมอยู่ใน commit 9bf7bfc).

## Mobile / accessibility / runtime QA sweep (Chromium headless, viewport 360/390/430/1440)

- [x] Build Card: ลบแท็ก `<script>` ซ้ำใน `templates/build_card.html` ที่ทำให้ JavaScript ทั้งหน้าไม่ทำงาน
- [x] CLI Surgeon: ปุ่ม Analyze ไม่ลบ `#rulesEmpty` อีกต่อไป (เดิม `renderRules` พ่น TypeError)
- [x] Flight Quiz: กันการเลื่อนข้อซ้ำเมื่อเลือกคำตอบ (auto-advance 380ms) แล้วกด Next ทันที
- [x] FPV Hub: ไอคอน Font Awesome ถูก CSP บล็อก → เปลี่ยนเป็น inline SVG (ไม่แก้ CSP)
- [x] BF Wizard: แก้ `@media(max-width: min(...))` ที่ไม่ถูกต้อง 6 จุด → ไม่มี overflow ที่ 360/390/430px
- [x] OSD Designer: grid มือถือใช้ `minmax(0,1fr)` + `min-width:0` → ไม่มี overflow
- [x] Accessibility: เพิ่ม `for` ให้ `<label>` 87 จุด, aria-label ช่อง PID ใน Tuning Log, สคริปต์ตั้งชื่อ control ที่ไม่มี label ใน `base.html`, landmark `<main>` ทุกหน้า, `<h1>` ในหน้า 404
- [x] Regression tests: `tests/test_mobile_a11y_regressions.py`
- [ ] ยังไม่ได้ตรวจ: FPV Simulator (three.js) / กราฟ Chart.js / gamepad (CDN ใช้ไม่ได้ในสภาพแวดล้อมทดสอบ), หน้า 429/500 ในเบราว์เซอร์, ขนาด touch target, toast ซ้อนกับ bottom nav บน `/osd` ที่ 360px
