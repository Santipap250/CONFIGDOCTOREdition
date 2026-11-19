import hashlib
import json
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
VIDEO_FILENAME_PATTERN = re.compile(r"landing-background-([a-f0-9]{12})\.mp4$")


def test_landing_video_is_deferred_and_retains_user_opt_outs(client):
    response = client.get("/landing")
    assert response.status_code == 200
    html = response.get_data(as_text=True)

    video_tag = re.search(r'<video[^>]*id="hero-background-video"[^>]*>', html)
    assert video_tag
    assert 'preload="none"' in video_tag.group(0)
    assert 'poster="/static/img/landing-background-poster.webp"' in video_tag.group(0)
    assert 'data-src="/static/video/landing-background-58e10cdf293b.mp4"' in html
    assert "requestIdleCallback" in html
    assert "addEventListener('load'" in html
    assert "window.setTimeout" in html
    assert "prefers-reduced-motion: reduce" in html
    assert "max-width: 760px" in html
    assert "connection.saveData" in html
    assert "effectiveType" in html
    assert "observer.observe(video)" in html


def test_landing_video_fingerprint_matches_identical_source_and_public_assets(client):
    html = client.get("/landing").get_data(as_text=True)
    match = re.search(
        r'data-src="/static/video/(landing-background-[a-f0-9]{12}\.mp4)"', html
    )
    assert match
    filename = match.group(1)
    assert VIDEO_FILENAME_PATTERN.search(filename)

    source_path = PROJECT_ROOT / "static" / "video" / filename
    public_path = PROJECT_ROOT / "public" / "static" / "video" / filename
    source_bytes = source_path.read_bytes()
    assert source_bytes == public_path.read_bytes()
    assert len(source_bytes) < 3_000_000
    expected_fingerprint = VIDEO_FILENAME_PATTERN.search(filename).group(1)
    actual_fingerprint = hashlib.sha256(source_bytes).hexdigest()[:12]
    assert actual_fingerprint == expected_fingerprint

    response = client.head(f"/static/video/{filename}")
    assert response.status_code == 200
    assert int(response.headers["Content-Length"]) == len(source_bytes)


def test_landing_video_cache_policy_is_long_lived_and_scoped_to_fingerprint():
    filename = "landing-background-58e10cdf293b.mp4"
    config = json.loads((PROJECT_ROOT / "vercel.json").read_text())
    matching_rules = [
        rule for rule in config["headers"]
        if rule.get("source") == f"/static/video/{filename}"
    ]
    assert len(matching_rules) == 1
    headers = {item["key"].lower(): item["value"] for item in matching_rules[0]["headers"]}
    assert headers["cache-control"] == "public, max-age=31536000, immutable"
