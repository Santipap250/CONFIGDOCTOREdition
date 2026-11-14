# blueprints/tools_static.py
# ── Tool pages that are pure render_template with no server-side logic.
#    Anything that touches request.form/args, the analyzer modules, or
#    module-level state stays in app.py — see the audit report for the
#    phased plan to migrate the remaining logic-bearing routes. ──────────
from flask import Blueprint, render_template, redirect

bp = Blueprint('tools_static', __name__)


# Landing-page catalog: every entry points to an existing Flask page endpoint.
# Keep this list limited to user-facing pages (not APIs, health checks, or assets).
HOME_TOOL_GROUPS = [
    {
        "id": "analysis",
        "title": "วิเคราะห์และจัดการคอนฟิก",
        "eyebrow": "ANALYZE",
        "tools": [
            {"title": "Drone Analyzer", "endpoint": "tools_analysis.index", "glyph": "AN", "summary": "วิเคราะห์สเปกโดรน พร้อมแนวทาง PID, Filter และประสิทธิภาพ", "keywords": "analyzer pid filter motor build"},
            {"title": "Blackbox CSV Analyzer", "endpoint": "tools_static.blackbox_page", "glyph": "BB", "summary": "อ่าน flight log เพื่อช่วยตรวจพฤติกรรมการบิน", "keywords": "blackbox csv log flight data"},
            {"title": "CLI Surgeon", "endpoint": "tools_static.cli_surgeon_page", "glyph": "CLI", "summary": "ตรวจ diff หรือ dump และทำความเข้าใจค่าคอนฟิก", "keywords": "cli diff dump configuration"},
            {"title": "CLI Diff Comparator", "endpoint": "tools_static.cli_comparator", "glyph": "Δ", "summary": "เปรียบเทียบ CLI สองชุดและดูค่าที่เปลี่ยน", "keywords": "cli compare comparator diff"},
            {"title": "Tuning Log", "endpoint": "tools_static.tuning_log", "glyph": "LOG", "summary": "บันทึกและทบทวนเซสชันการจูน", "keywords": "tuning history session pid"},
            {"title": "Build Card Generator", "endpoint": "tools_static.build_card", "glyph": "BLD", "summary": "จัดทำการ์ดสรุปสเปก build สำหรับแชร์", "keywords": "build card spec share"},
            {"title": "OSD Designer", "endpoint": "tools_static.osd_page", "glyph": "OSD", "summary": "จัดวางข้อมูล OSD และสร้าง CLI สำหรับส่งออก", "keywords": "osd layout export cli"},
        ],
    },
    {
        "id": "tuning",
        "title": "ตั้งค่าและจูนการบิน",
        "eyebrow": "TUNE",
        "tools": [
            {"title": "PID Symptom Advisor", "endpoint": "tools_advisor.pid_advisor", "glyph": "PID", "summary": "เลือกอาการที่พบเพื่อดูแนวทางตรวจและปรับ PID", "keywords": "pid advisor propwash oscillation bounce"},
            {"title": "Quick Tune Pad", "endpoint": "tools_advisor.quick_tune", "glyph": "QT", "summary": "สร้างแนวทางปรับค่าแบบรวดเร็วจากอาการ", "keywords": "quick tune pid cli"},
            {"title": "RPM Filter Calculator", "endpoint": "tools_rpm.rpm_filter", "glyph": "RPM", "summary": "คำนวณค่าและช่วงที่เกี่ยวข้องกับ RPM filter", "keywords": "rpm filter harmonic notch"},
            {"title": "Rates Visualizer", "endpoint": "tools_static.rates_visualizer", "glyph": "RTE", "summary": "ดูเส้นโค้ง rates และผลของค่าต่อการควบคุม", "keywords": "rates visualizer curve expo rc rate"},
            {"title": "Betaflight Config Wizard", "endpoint": "tools_static.bf_wizard", "glyph": "BF", "summary": "ไล่ตั้งค่าทีละขั้นและสร้าง CLI ตามตัวเลือก", "keywords": "betaflight wizard setup config"},
        ],
    },
    {
        "id": "hardware",
        "title": "ตรวจสอบฮาร์ดแวร์และพลังงาน",
        "eyebrow": "HARDWARE",
        "tools": [
            {"title": "Motor × Prop Recommender", "endpoint": "tools_analysis.motor_prop", "glyph": "M×P", "summary": "สำรวจความเหมาะสมของมอเตอร์ ใบพัด และแบตเตอรี่", "keywords": "motor prop kv stator battery"},
            {"title": "ESC Compatibility Checker", "endpoint": "tools_static.esc_checker", "glyph": "ESC", "summary": "ตรวจข้อมูล ESC, กระแส และโปรโตคอลที่เกี่ยวข้อง", "keywords": "esc compatibility dshot protocol amps"},
            {"title": "Battery Health Advisor", "endpoint": "tools_static.battery_health", "glyph": "BAT", "summary": "ประเมิน IR, voltage sag และสุขภาพแบตเตอรี่", "keywords": "battery health ir sag lipo"},
            {"title": "Motor Thermal Estimator", "endpoint": "tools_static.motor_thermal", "glyph": "°C", "summary": "ประเมินแนวโน้มอุณหภูมิและ thermal margin ของมอเตอร์", "keywords": "motor thermal temperature winding"},
            {"title": "Control Loop Analyzer", "endpoint": "tools_static.loop_analyzer", "glyph": "LOOP", "summary": "สำรวจ latency ในเส้นทางควบคุมจาก stick ถึง prop", "keywords": "control loop latency looptime"},
        ],
    },
    {
        "id": "video",
        "title": "วิดีโอและสัญญาณ",
        "eyebrow": "VIDEO · RF",
        "tools": [
            {"title": "VTX Bands & Channels", "endpoint": "tools_vtx.vtx", "glyph": "VTX", "summary": "ค้นตาราง band/channel และข้อมูลกำลังส่ง", "keywords": "vtx band channel frequency"},
            {"title": "VTX Range Calculator", "endpoint": "tools_vtx.vtx_range", "glyph": "RF", "summary": "ประมาณระยะสัญญาณจากเงื่อนไขการใช้งาน", "keywords": "vtx range signal calculator"},
            {"title": "SmartAudio / Tramp Guide", "endpoint": "tools_vtx.vtx_smartaudio", "glyph": "SA", "summary": "อ้างอิงคำสั่งและการตั้งค่าระบบควบคุม VTX", "keywords": "smartaudio tramp commands vtx"},
        ],
    },
    {
        "id": "discover",
        "title": "ฝึกบินและค้นพบเพิ่มเติม",
        "eyebrow": "EXPLORE",
        "tools": [
            {"title": "FPV Training Simulator", "endpoint": "tools_static.fpv_trainer", "glyph": "SIM", "summary": "ฝึกการควบคุมผ่านซิมูเลเตอร์ FPV บนเว็บ", "keywords": "fpv trainer simulator practice gamepad"},
            {"title": "Flight Style Quiz", "endpoint": "tools_static.flight_quiz", "glyph": "QUIZ", "summary": "สำรวจสไตล์การบินและดูคำแนะนำที่เกี่ยวข้อง", "keywords": "flight style quiz rates"},
            {"title": "Military UAS Analyzer", "endpoint": "content_pages.military_uas", "glyph": "UAS", "summary": "เครื่องมือวิเคราะห์ข้อมูลอากาศยานไร้คนขับเฉพาะทาง", "keywords": "military uas aircraft analysis"},
            {"title": "Config Leaderboard", "endpoint": "tools_static.leaderboard", "glyph": "TOP", "summary": "สำรวจและโหวตคอนฟิกจากชุมชน", "keywords": "config leaderboard community vote"},
            {"title": "FPV Knowledge Hub", "endpoint": "tools_static.fpv_hub", "glyph": "HUB", "summary": "รวมบทความและทางลัดความรู้ FPV", "keywords": "fpv knowledge hub articles learn"},
        ],
    },
    {
        "id": "resources",
        "title": "คู่มือและข้อมูลประกอบ",
        "eyebrow": "RESOURCES",
        "tools": [
            {"title": "FPV Gear Guide", "endpoint": "tools_gear.fpv_gear", "glyph": "GEAR", "summary": "ดูแนวทางเลือกอุปกรณ์ตามประเภทและสไตล์การบิน", "keywords": "gear guide parts frame prop"},
            {"title": "CLI Downloads", "endpoint": "downloads.downloads_index", "glyph": "FILE", "summary": "เรียกดูไฟล์ DIFF และ DUMP ที่เตรียมไว้", "keywords": "downloads diff dump files"},
            {"title": "About CONFIGDOCTOR", "endpoint": "content_pages.about", "glyph": "INFO", "summary": "ทำความรู้จักเว็บไซต์และแนวทางการใช้งาน", "keywords": "about information"},
            {"title": "Team", "endpoint": "content_pages.team", "glyph": "TEAM", "summary": "ข้อมูลทีมและผู้พัฒนาโครงการ", "keywords": "team developers"},
            {"title": "Changelog", "endpoint": "content_pages.changelog", "glyph": "LOG", "summary": "ติดตามบันทึกการเปลี่ยนแปลงของเว็บไซต์", "keywords": "changelog updates release"},
        ],
    },
]


@bp.route("/landing")
def landing():
    tool_count = sum(len(group["tools"]) for group in HOME_TOOL_GROUPS)
    return render_template("landing.html", tool_groups=HOME_TOOL_GROUPS, tool_count=tool_count)


@bp.route("/")
def loading():
    # Keep the root URL as a direct route to the main workspace landing page.
    return redirect("/landing", code=302)


@bp.route("/ping")
def ping():
    return "pong"


@bp.route('/fpv')
def fpv_hub():
    return render_template('fpv/index.html')


@bp.route('/cli_surgeon')
def cli_surgeon_page():
    return render_template('cli_surgeon.html')


@bp.route('/rates-visualizer')
def rates_visualizer():
    return render_template('rates_visualizer.html')


@bp.route('/cli-comparator')
def cli_comparator():
    return render_template('cli_comparator.html')


@bp.route('/blackbox')
def blackbox_page():
    return render_template('blackbox.html')


@bp.route('/esc-checker')
def esc_checker():
    return render_template('esc_checker.html')


@bp.route('/fpv-trainer')
def fpv_trainer():
    return render_template('fpv_trainer.html')


@bp.route('/flight-quiz')
def flight_quiz():
    """Flight Style Quiz — 5 questions, recommends rates + preset"""
    return render_template('flight_quiz.html')


@bp.route('/bf-wizard')
def bf_wizard():
    """Betaflight Config Wizard — 7 steps → CLI ready to paste"""
    return render_template('bf_wizard.html')


@bp.route('/build-card')
def build_card():
    """Build Card Generator — shareable drone spec card"""
    return render_template('build_card.html')


@bp.route('/tuning-log')
def tuning_log():
    """Tuning Log — records every tuning session"""
    return render_template('tuning_log.html')


@bp.route('/leaderboard')
def leaderboard():
    """Community Config Leaderboard — vote + rank configs"""
    return render_template('leaderboard.html')


@bp.route('/battery-health')
def battery_health():
    return render_template('battery_health.html')


@bp.route('/motor-thermal')
def motor_thermal():
    return render_template('motor_thermal.html')


@bp.route('/loop-analyzer')
def loop_analyzer():
    return render_template('loop_analyzer.html')


@bp.route('/osd')
def osd_page():
    return render_template('osd.html')
