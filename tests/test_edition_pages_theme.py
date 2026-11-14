from pathlib import Path
import re

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]

PAGE_ROUTES = [
    "/app",
    "/landing",
    "/about",
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
    assert "/static/css/edition-pages.css" in html

    # The shared override is emitted after any page-specific CSS in the head.
    head = html.split("</head>", 1)[0]
    stylesheet_hrefs = re.findall(
        r'<link\b(?=[^>]*\brel=["\']stylesheet["\'])[^>]*\bhref=["\']([^"\']+)',
        head,
        re.I,
    )
    assert stylesheet_hrefs[-1].endswith("/static/css/edition-pages.css")


def test_edition_page_stylesheet_is_scoped_away_from_the_homepage():
    css = (PROJECT_ROOT / "static/css/edition-pages.css").read_text()

    assert "body:not(.landing-page)" in css
    assert "#08110f" in css
    assert "#75e3b4" in css


def test_edition_stylesheet_public_mirror_matches_source():
    source = (PROJECT_ROOT / "static/css/edition-pages.css").read_bytes()
    public = (PROJECT_ROOT / "public/static/css/edition-pages.css").read_bytes()

    assert source == public


@pytest.mark.parametrize("route", ["/pid-advisor", "/cli_surgeon", "/blackbox", "/motor-prop", "/landing"])
def test_page_title_uses_edition_brand(client, route):
    response = client.get(route)
    assert response.status_code == 200

    title = re.search(r"<title>(.*?)</title>", response.get_data(as_text=True), re.S | re.I)
    assert title is not None
    assert "CONFIGDOCTOR Edition" in title.group(1)
