import re
import xml.etree.ElementTree as ET
from pathlib import Path

from blueprints import tools_static


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_elite_stylesheet_is_loaded_after_premium_and_mirrored(client):
    response = client.get("/landing")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    premium = html.index('href="/static/css/landing-premium.css"')
    elite = html.index('href="/static/css/landing-elite.css"')
    assert elite > premium

    css_response = client.get("/static/css/landing-elite.css")
    assert css_response.status_code == 200
    source = css_response.get_data()
    public_mirror = (PROJECT_ROOT / "public/static/css/landing-elite.css").read_bytes()
    assert source == public_mirror
    assert b"@import" not in source
    assert b"prefers-reduced-motion" in source
    assert b"body.landing-page.light" in source
    assert b"--elite-dim:" in source


def test_landing_motion_assets_are_served_mirrored_and_accessible(client):
    response = client.get("/landing")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    elite_css = html.index('href="/static/css/landing-elite.css"')
    motion_css = html.index('href="/static/css/landing-motion.css"')
    assert motion_css > elite_css
    assert 'src="/static/js/landing-motion.js"' in html

    css_response = client.get("/static/css/landing-motion.css")
    js_response = client.get("/static/js/landing-motion.js")
    assert css_response.status_code == 200
    assert js_response.status_code == 200
    assert css_response.data == (
        PROJECT_ROOT / "public/static/css/landing-motion.css"
    ).read_bytes()
    assert js_response.data == (
        PROJECT_ROOT / "public/static/js/landing-motion.js"
    ).read_bytes()
    assert b"elite-orbit-flight" in css_response.data
    assert b"prefers-reduced-motion: reduce" in css_response.data
    assert b"IntersectionObserver" in js_response.data
    assert b"prefers-reduced-motion" in js_response.data


def test_tool_artwork_covers_each_live_tool_with_unique_vector_symbols(client):
    response = client.get("/landing")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    tools = [tool for group in tools_static.TOOL_CENTER_GROUPS for tool in group["tools"]]
    expected_ids = [tool["endpoint"].replace(".", "-") for tool in tools]
    card_ids = re.findall(r'data-art-id="([^"]+)"', html)
    assert card_ids == expected_ids
    assert len(set(card_ids)) == len(tools) == 30
    for art_id in expected_ids:
        assert f"#art-{art_id}" in html
        assert f"#icon-{art_id}" in html

    sprite_response = client.get("/static/img/tool-artwork-sprite.svg")
    assert sprite_response.status_code == 200
    sprite_path = PROJECT_ROOT / "static/img/tool-artwork-sprite.svg"
    public_path = PROJECT_ROOT / "public/static/img/tool-artwork-sprite.svg"
    assert sprite_response.data == sprite_path.read_bytes() == public_path.read_bytes()

    root = ET.fromstring(sprite_response.data)
    namespace = "{http://www.w3.org/2000/svg}"
    symbols = root.findall(f".//{namespace}symbol")
    symbol_ids = {symbol.get("id") for symbol in symbols}
    assert len(symbols) == 60
    assert all(f"icon-{art_id}" in symbol_ids for art_id in expected_ids)
    assert all(f"art-{art_id}" in symbol_ids for art_id in expected_ids)
    icon_markup = {
        ET.tostring(symbol, encoding="unicode")
        for symbol in symbols
        if symbol.get("id", "").startswith("icon-")
    }
    art_markup = {
        ET.tostring(symbol, encoding="unicode")
        for symbol in symbols
        if symbol.get("id", "").startswith("art-")
    }
    assert len(icon_markup) == len(art_markup) == len(tools)


def test_tool_art_stylesheet_loads_after_motion_and_is_mirrored(client):
    response = client.get("/landing")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    motion = html.index('href="/static/css/landing-motion.css"')
    artwork = html.index('href="/static/css/landing-tool-art.css"')
    assert artwork > motion

    css_response = client.get("/static/css/landing-tool-art.css")
    assert css_response.status_code == 200
    assert css_response.data == (
        PROJECT_ROOT / "public/static/css/landing-tool-art.css"
    ).read_bytes()
    assert b"tool-art-sweep" in css_response.data
    assert b"prefers-reduced-motion: no-preference" in css_response.data
    assert b"prefers-reduced-motion: reduce" in css_response.data


def test_elite_signal_strip_uses_live_counts_and_truthful_saved_label(client, monkeypatch):
    groups = tools_static.TOOL_CENTER_GROUPS[:2]
    monkeypatch.setattr(tools_static, "TOOL_CENTER_GROUPS", groups)
    expected_tools = sum(len(group["tools"]) for group in groups)

    response = client.get("/landing")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    match = re.search(
        r'<section class="elite-signal-strip\b.*?</section>', html, re.DOTALL
    )
    assert match
    values = re.findall(
        r'<span class="elite-stat-value">(.*?)</span>', match.group(0), re.DOTALL
    )
    assert values == [str(expected_tools), f"{len(groups):02d}", "LOCAL"]
    assert 'data-label-th="บันทึกไว้ในอุปกรณ์นี้"' in match.group(0)
    assert 'data-label-en="SAVED ON DEVICE"' in match.group(0)
