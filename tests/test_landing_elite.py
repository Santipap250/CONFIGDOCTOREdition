import re
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
