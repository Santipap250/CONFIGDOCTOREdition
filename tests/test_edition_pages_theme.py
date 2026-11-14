from pathlib import Path
import re

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]

PAGE_ROUTES = [
    "/app",
    "/landing",
    "/about",
    "/team",
    "/changelog",
    "/downloads",
    "/vtx",
    "/vtx-range",
    "/vtx-smartaudio",
    "/motor-prop",
    "/cli_surgeon",
    "/pid-advisor",
    "/quick-tune",
    "/rpm-filter",
    "/rates-visualizer",
    "/cli-comparator",
    "/blackbox",
    "/esc-checker",
    "/fpv-trainer",
    "/osd",
    "/battery-health",
    "/motor-thermal",
    "/loop-analyzer",
    "/flight-quiz",
    "/bf-wizard",
    "/build-card",
    "/tuning-log",
    "/leaderboard",
    "/military-uas",
    "/fpv",
    "/fpv-gear",
]


@pytest.mark.parametrize("route", PAGE_ROUTES)
def test_application_pages_load_edition_stylesheet(client, route):
    response = client.get(route)

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "/static/css/edition-tokens.css" in html
    assert "/static/css/edition-pages.css" in html

    # The shared override is emitted after any page-specific CSS in the head.
    head = html.split("</head>", 1)[0]
    stylesheet_hrefs = re.findall(
        r'<link\b(?=[^>]*\brel=["\']stylesheet["\'])[^>]*\bhref=["\']([^"\']+)',
        head,
        re.I,
    )
    assert stylesheet_hrefs[-1].endswith("/static/css/edition-pages.css")
    token_index = next(i for i, href in enumerate(stylesheet_hrefs) if href.endswith("/static/css/edition-tokens.css"))
    theme_index = next(i for i, href in enumerate(stylesheet_hrefs) if href.endswith("/static/css/edition-pages.css"))
    assert token_index < theme_index


def test_edition_page_stylesheet_is_scoped_away_from_the_homepage():
    css = (PROJECT_ROOT / "static/css/edition-pages.css").read_text()

    assert "body:not(.landing-page)" in css
    assert "var(--cd-bg)" in css
    assert "var(--cd-accent)" in css


def test_landing_body_class_is_rendered_for_theme_scope(client):
    response = client.get("/landing")

    assert response.status_code == 200
    assert '<body class="landing-page">' in response.get_data(as_text=True)


def test_edition_stylesheet_public_mirror_matches_source():
    source = (PROJECT_ROOT / "static/css/edition-pages.css").read_bytes()
    public = (PROJECT_ROOT / "public/static/css/edition-pages.css").read_bytes()

    assert source == public


def test_canonical_tokens_are_shared_and_mirrored():
    source = (PROJECT_ROOT / "static/css/edition-tokens.css").read_bytes()
    public = (PROJECT_ROOT / "public/static/css/edition-tokens.css").read_bytes()
    css = source.decode("utf-8")

    assert source == public
    assert "--cd-bg: #08110f" in css
    assert "--cd-accent: #75e3b4" in css
    assert "--cd-heading: 'Manrope'" in css
    assert "--cd-body: 'Sarabun'" in css
    assert "--cd-mono: 'DM Mono'" in css


@pytest.mark.parametrize("route", ["/app", "/pid-advisor", "/fpv-trainer", "/fpv"])
def test_mobile_shared_header_identifies_edition_and_current_page(client, route):
    response = client.get(route)

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert '<header class="pa-mbar"' in html
    assert 'class="pa-mbrand"' in html
    assert "CONFIGDOCTOR" in html
    assert 'class="pa-page-title" aria-current="page"' in html


@pytest.mark.parametrize("route", ["/app", "/pid-advisor", "/blackbox", "/fpv-trainer"])
def test_core_tools_have_one_accessible_page_heading(client, route):
    response = client.get(route)

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert len(re.findall(r"<h1\b", html, re.I)) == 1

    if route in {"/app", "/fpv-trainer"}:
        assert "class=\"cd-sr-only\"" in html


@pytest.mark.parametrize(
    ("template_name", "status_class"),
    [("404.html", "error-page"), ("429.html", "error-429"), ("500.html", "error-500")],
)
def test_standalone_error_templates_load_shared_theme(client, template_name, status_class):
    from flask import render_template

    with client.application.test_request_context():
        html = render_template(template_name)

    assert "/static/css/edition-tokens.css" in html
    assert "/static/css/edition-pages.css" in html
    assert f'class="{status_class}"' in html
    if template_name in {"429.html", "500.html"}:
        assert "--font-d:var(--cd-mono);" in html or "--font-d: var(--cd-mono);" in html


def test_fpv_knowledge_hub_uses_edition_palette(client):
    response = client.get("/fpv")

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "--bg-color: var(--cd-bg);" in html
    assert "--primary: var(--cd-accent);" in html
    assert 'class="hub-cta hub-cta-primary"' in html
    source = (PROJECT_ROOT / "templates" / "fpv" / "index.html").read_text(encoding="utf-8")
    for legacy_color in ("#0f172a", "#1e293b", "#38bdf8", "#f43f5e", "#334155", "#475569", "#10c47a"):
        assert legacy_color not in source


def test_not_found_response_uses_themed_404_page(client):
    response = client.get("/theme-test-route-that-does-not-exist")

    assert response.status_code == 404
    assert "/static/css/edition-pages.css" in response.get_data(as_text=True)


@pytest.mark.parametrize("route", ["/pid-advisor", "/cli_surgeon", "/blackbox", "/motor-prop", "/landing"])
def test_page_title_uses_edition_brand(client, route):
    response = client.get(route)
    assert response.status_code == 200

    title = re.search(r"<title>(.*?)</title>", response.get_data(as_text=True), re.S | re.I)
    assert title is not None
    assert "CONFIGDOCTOR Edition" in title.group(1)
