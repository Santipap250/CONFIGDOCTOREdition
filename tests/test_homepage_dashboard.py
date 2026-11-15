import re
from html.parser import HTMLParser
from pathlib import Path

from flask import url_for

from blueprints.tools_static import HOME_TOOL_GROUPS
from core import _BASE_URL


class _HeadTextParser(HTMLParser):
    """Collect unwrapped text nodes inside head (title/script/style are expected)."""

    def __init__(self):
        super().__init__()
        self.in_head = False
        self.suppressed = 0
        self.unwrapped_text = []

    def handle_starttag(self, tag, attrs):
        if tag == "head":
            self.in_head = True
        elif self.in_head and tag in {"title", "script", "style"}:
            self.suppressed += 1

    def handle_endtag(self, tag):
        if self.in_head and tag in {"title", "script", "style"} and self.suppressed:
            self.suppressed -= 1
        elif tag == "head":
            self.in_head = False

    def handle_data(self, data):
        if self.in_head and not self.suppressed and data.strip():
            self.unwrapped_text.append(data.strip())


def test_landing_uses_configdoctor_edition_brand_and_metadata(client):
    response = client.get("/landing")

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "<title>CONFIGDOCTOR Edition | FPV Flight Workspace</title>" in html
    assert 'content="CONFIGDOCTOR Edition"' in html
    assert 'id="hero-title"' in html
    assert 'id="tool-search"' in html
    assert 'aria-label="กรองเครื่องมือตามหมวด"' in html

    canonical = re.search(r'<link rel="canonical" href="([^"]+)"', html)
    assert canonical
    assert canonical.group(1) == f"{_BASE_URL}/landing"
    assert "configdoctor.onrender.com" not in canonical.group(1)

    parser = _HeadTextParser()
    parser.feed(html)
    assert parser.unwrapped_text == []


def test_landing_catalog_contains_every_existing_page_endpoint(client, app):
    response = client.get("/landing")
    assert response.status_code == 200
    html = response.get_data(as_text=True)

    tools = [tool for group in HOME_TOOL_GROUPS for tool in group["tools"]]
    assert len(tools) == 30
    assert f"<strong>{len(tools)}</strong><small>รายการ</small>" in html
    assert html.count('class="tool-card"') == len(tools)

    with app.test_request_context():
        for tool in tools:
            endpoint = tool["endpoint"]
            assert endpoint in app.view_functions, f"Unknown endpoint: {endpoint}"
            path = url_for(endpoint)
            assert f'href="{path}"' in html, f"Missing landing link for {endpoint}"


def test_workspace_navigation_has_five_destinations_and_four_tool_groups(client):
    html = client.get("/landing").get_data(as_text=True)
    for label in ("Home", "Tools", "Analyze", "Saved", "More"):
        assert f">{label}</span>" in html
    assert html.count('class="bnav-item') == 5
    for group in ("analyze", "tune", "build", "learn"):
        assert f'data-tool-group="{group}"' in html
        assert f'data-filter="{group}"' in html
    assert 'href="/landing#tools"' in html
    assert 'href="/app"' in html
    assert 'id="saved"' in html
    assert "ไม่ซิงก์ข้ามอุปกรณ์" in html


def test_desktop_more_pages_do_not_mark_tools_and_more_as_current_together(client):
    html = client.get("/fpv-gear").get_data(as_text=True)
    tools_link = re.search(r'<a data-workspace-link="tools"[^>]*>', html)
    more_menu = re.search(r'<details class="workspace-more"[^>]*>', html)
    assert tools_link and 'aria-current="page"' not in tools_link.group(0)
    assert more_menu and 'data-current="true"' in more_menu.group(0)


def test_legacy_theme_and_menu_language_controls_remain_available(client):
    landing = client.get("/landing").get_data(as_text=True)
    tool_page = client.get("/fpv-gear").get_data(as_text=True)

    for html in (landing, tool_page):
        assert 'data-theme-toggle' in html
        assert 'data-language-toggle' in html
        assert "obix-theme" in html
        assert "obix-lang" in html
        assert "localStorage.setItem" in html
    assert 'data-label-th="เครื่องมือ" data-label-en="Tools"' in landing
    assert 'data-label-th="ภาพรวม" data-label-en="Overview"' in landing
    assert landing.count('class="bnav-item') == 5


def test_analyzer_uses_shared_tool_center_without_duplicate_modal(client):
    html = client.get("/app").get_data(as_text=True)
    assert 'data-workspace-tab="analyze"' in html
    assert 'id="toolsModal"' not in html
    assert "var TOOLS = [" not in html
    assert "openToolsModal" not in html
    assert 'id="aForm"' in html
    assert "window.liveCalc=function()" in html


def test_fpv_hub_canonical_uses_the_shared_base_url(client):
    response = client.get("/fpv")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert f'href="{_BASE_URL}/fpv"' in html
    assert "https://configdoctor.onrender.com/fpv" not in html


def test_landing_css_source_matches_vercel_public_mirror():
    project_root = Path(__file__).resolve().parents[1]
    source_css = (project_root / "static/css/landing-premium.css").read_bytes()
    public_css = (project_root / "public/static/css/landing-premium.css").read_bytes()
    assert source_css == public_css
