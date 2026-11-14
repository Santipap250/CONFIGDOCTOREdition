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
