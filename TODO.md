# CONFIGDOCTOR Edition — Full Application Design TODO

สถานะ: unified redesign ผ่าน PR #9 ซึ่งบัญชีเจ้าของ repository merge แล้ว; follow-up ปรับ mobile simulator 1px ยังรอตรวจ Preview/อนุมัติแยกต่างหาก

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
- [ ] ยังไม่ได้ทำ manual JavaScript console/runtime-error sweep สำหรับทุก interaction หลัง visual update; full automated test suite ผ่าน.
- [ ] Follow-up mobile Simulator height fix (56px header clearance) ต้องตรวจบน Vercel Preview ล่าสุดก่อน; ห้าม merge/deploy follow-up จนผู้ใช้ตรวจและอนุมัติ.