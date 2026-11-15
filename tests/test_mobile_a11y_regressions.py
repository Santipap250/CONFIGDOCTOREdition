# tests/test_mobile_a11y_regressions.py — CONFIGDOCTOR Edition
# Regression tests for defects found during the mobile / accessibility / runtime QA sweep.
# Source-level checks only (no browser needed), so they run anywhere pytest runs.
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = sorted((ROOT / "templates").rglob("*.html"))


def _read(p):
    return Path(p).read_text(encoding="utf-8")


def test_every_template_has_balanced_script_tags():
    """build_card.html once had a duplicated <script> opener that killed all page JS."""
    for path in TEMPLATES:
        s = _read(path)
        assert len(re.findall(r"<script\b", s)) == len(re.findall(r"</script>", s)), path.name
        assert not re.search(r"<script[^>]*>\s*<script\b", s), f"double <script> in {path.name}"


def test_no_invalid_min_function_in_media_queries():
    """`@media(max-width: min(980px,100%))` is invalid, never matches, and broke bf-wizard on phones."""
    pattern = re.compile(r"@media\s*\(\s*(?:max|min)-width\s*:\s*min\(")
    files = TEMPLATES + sorted((ROOT / "static" / "css").glob("*.css"))
    for path in files:
        assert not pattern.search(_read(path)), path.name


def test_stylesheets_only_from_hosts_allowed_by_csp():
    """CSP style-src allows only 'self', inline and Google Fonts; other CDN stylesheets are silently blocked."""
    link = re.compile(r"<link[^>]+rel=[\"']stylesheet[\"'][^>]*href=[\"']https?://([^/\"']+)", re.I)
    for path in TEMPLATES:
        for host in link.findall(_read(path)):
            assert host in {"fonts.googleapis.com", "fonts.gstatic.com"}, f"{path.name}: {host}"


def test_fpv_hub_uses_inline_svg_icons_not_blocked_font_awesome():
    s = _read(ROOT / "templates" / "fpv" / "index.html")
    assert "font-awesome" not in s
    assert 'class="fas ' not in s
    assert s.count('class="fpv-ico"') >= 10


def test_label_for_targets_exist():
    """Every static <label for="x"> must point at an id that exists in the same template."""
    for path in TEMPLATES:
        s = _read(path)
        ids = set(re.findall(r"\bid=[\"']([^\"'{}]+)[\"']", s))
        for target in re.findall(r"<label[^>]*\bfor=[\"']([^\"'{}]+)[\"']", s):
            assert target in ids, f"{path.name}: label for={target} has no matching id"


def test_base_template_names_unlabeled_controls():
    s = _read(ROOT / "templates" / "base.html")
    assert "data-a11y-auto" in s
    assert "aria-labelledby" in s  # never overrides existing accessible names


def test_tuning_log_pid_inputs_have_explicit_names():
    s = _read(ROOT / "templates" / "tuning_log.html")
    for axis in ("Roll", "Pitch", "Yaw"):
        for term in ("P", "I", "D"):
            assert f'aria-label="{axis} {term} gain"' in s


def test_cli_surgeon_scan_does_not_destroy_empty_state_node():
    """Analyze used to wipe #rulesList (incl. #rulesEmpty) and then renderRules threw a TypeError."""
    s = _read(ROOT / "templates" / "cli_surgeon.html")
    assert "getElementById('rulesList').innerHTML" not in s
    assert "scan-placeholder" in s
    assert "if (emptyEl) emptyEl.style.display" in s


def test_flight_quiz_navigation_is_guarded_against_double_advance():
    """Select (380 ms auto-advance) + tapping Next used to advance twice and read QUESTIONS[n].label."""
    s = _read(ROOT / "templates" / "flight_quiz.html")
    assert "let navBusy = false;" in s
    assert s.count("if (navBusy) return;") >= 2
    assert "state.step >= QUESTIONS.length - 1" in s
    assert "let autoAdvanceTimer = null;" in s
    assert "clearTimeout(autoAdvanceTimer);" in s


def test_rates_visualizer_range_controls_have_accessible_names():
    s = _read(ROOT / "templates" / "rates_visualizer.html")
    ranges = re.findall(r"<input\b(?=[^>]*\btype=[\"']range[\"'])([^>]*)>", s)
    assert ranges
    assert all(re.search(r"\baria-label=[\"'][^\"']+[\"']", attrs) for attrs in ranges)


def test_flight_quiz_choices_are_keyboard_operable_and_zoom_is_allowed():
    s = _read(ROOT / "templates" / "flight_quiz.html")
    assert "maximum-scale=1.0" not in s
    assert 'role="radiogroup" aria-labelledby="question-label"' in s
    assert 'role="radio" aria-checked=' in s
    assert "handleChoiceKey(event" in s and "event.key === 'ArrowRight'" in s
    assert "prefers-reduced-motion:reduce" in s


def test_legacy_custom_buttons_support_enter_and_space():
    s = _read(ROOT / "templates" / "base.html")
    assert "event.key === 'Enter'" in s
    assert "event.key === ' '" in s
    assert "control.click()" in s


def test_osd_and_wizard_grids_can_shrink_on_mobile():
    osd = _read(ROOT / "templates" / "osd.html")
    assert "grid-template-columns:minmax(0,1fr)" in osd
    assert ".studio-wrap>*" in osd and "min-width:0" in osd


def test_page_routes_still_render(client):
    for path in ("/build-card", "/fpv", "/bf-wizard", "/osd", "/cli_surgeon", "/flight-quiz", "/tuning-log"):
        assert client.get(path).status_code == 200, path


def test_base_wraps_content_in_a_single_main_landmark():
    base = _read(ROOT / "templates" / "base.html")
    assert '<main id="main-content">' in base and "block main_close" in base
    # pages that already ship their own <main> must opt out so there is never a second one
    for name in ("landing.html", "fpv_gear.html", "pid_advisor.html"):
        s = _read(ROOT / "templates" / name)
        assert "{% block main_open %}{% endblock %}" in s, name
        assert "{% block main_close %}{% endblock %}" in s, name


def test_error_pages_and_fpv_hub_expose_main_and_h1():
    assert "<h1" in _read(ROOT / "templates" / "404.html")
    for name in ("404.html", "429.html", "500.html"):
        assert 'role="main"' in _read(ROOT / "templates" / name), name
    assert 'role="main"' in _read(ROOT / "templates" / "fpv" / "index.html")


def test_all_templates_compile_with_jinja():
    from jinja2 import Environment, FileSystemLoader
    env = Environment(loader=FileSystemLoader(str(ROOT / "templates")))
    env.globals["csrf_token"] = lambda: ""
    env.globals["url_for"] = lambda *a, **k: "/"
    for path in TEMPLATES:
        env.get_template(path.relative_to(ROOT / "templates").as_posix())


def test_429_and_500_cards_cannot_overflow_phone_viewports():
    for name in ("429.html", "500.html"):
        s = _read(ROOT / "templates" / name)
        card = re.search(r"\.card\s*\{[^}]*\}", s).group(0)
        assert "box-sizing: border-box" in card and "min-width: 0" in card, name


def test_base_wraps_content_in_a_single_main_landmark():
    base = _read(ROOT / "templates" / "base.html")
    assert '{% block main_open %}<main id="main-content">{% endblock %}' in base
    assert "{% block main_close %}</main>{% endblock %}" in base
    # Pages that already provide their own <main> must suppress the default wrapper.
    for name in ("landing.html", "fpv_gear.html", "pid_advisor.html"):
        s = _read(ROOT / "templates" / name)
        assert "{% block main_open %}{% endblock %}" in s and "{% block main_close %}{% endblock %}" in s, name


def test_rendered_pages_have_exactly_one_main_landmark(client):
    pages = ("/app", "/about", "/bf-wizard", "/osd", "/cli_surgeon", "/flight-quiz", "/tuning-log",
             "/landing", "/pid-advisor", "/fpv-gear", "/fpv", "/build-card", "/vtx")
    for path in pages:
        html = client.get(path).get_data(as_text=True)
        n = len(re.findall(r"<main\b", html)) + len(re.findall(r'role="main"', html))
        assert n == 1, f"{path}: {n} main landmarks"


def test_error_pages_expose_main_and_heading(client):
    html = client.get("/definitely-not-a-page").get_data(as_text=True)
    assert 'role="main"' in html and "<h1" in html
    for name in ("429.html", "500.html"):
        s = _read(ROOT / "templates" / name)
        assert 'role="main"' in s and "<h1" in s, name
