import json
import struct
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _png_dimensions(data):
    assert data[:8] == b"\x89PNG\r\n\x1a\n"
    return struct.unpack(">II", data[16:24])


def test_manifest_is_linked_from_shared_page_head(client):
    response = client.get("/landing")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert 'rel="manifest" href="/manifest.json"' in html
    assert 'rel="apple-touch-icon"' in html
    assert "navigator.serviceWorker.register('/sw.js'" in html


def test_landing_uses_optimized_background_video_and_poster(client):
    response = client.get("/landing")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert 'class="hero-bg-video" id="hero-background-video" muted loop playsinline preload="none"' in html
    assert 'data-src="/static/video/landing-background.mp4"' in html
    assert 'autoplay' not in html
    assert "prefers-reduced-motion: reduce" in html
    assert "navigator.connection" in html
    assert '/static/img/landing-background-poster.webp' in html

    video = client.get("/static/video/landing-background.mp4")
    poster = client.get("/static/img/landing-background-poster.webp")
    assert video.status_code == 200
    assert video.mimetype == "video/mp4"
    assert poster.status_code == 200
    assert poster.mimetype == "image/webp"


def test_manifest_has_installable_start_scope_and_required_icons(client):
    response = client.get("/manifest.json")
    assert response.status_code == 200
    assert response.mimetype == "application/json"
    assert "max-age=3600" in response.headers.get("Cache-Control", "")

    manifest = json.loads(response.get_data(as_text=True))
    assert manifest["name"] == "CONFIGDOCTOR Edition — FPV Flight Workspace"
    assert manifest["short_name"] == "CONFIGDOCTOR"
    assert manifest["theme_color"] == "#08110f"
    assert manifest["background_color"] == "#08110f"
    assert manifest["start_url"] == "/landing"
    assert manifest["scope"] == "/"
    assert manifest["display"] == "standalone"

    icons = {icon["sizes"]: icon for icon in manifest["icons"] if icon.get("purpose") == "any"}
    assert "192x192" in icons
    assert "512x512" in icons
    for expected_size, icon in ((192, icons["192x192"]), (512, icons["512x512"])):
        asset = client.get(icon["src"])
        assert asset.status_code == 200, icon["src"]
        assert asset.mimetype == "image/png"
        assert _png_dimensions(asset.data) == (expected_size, expected_size)

    maskable = next(icon for icon in manifest["icons"] if icon.get("purpose") == "maskable")
    assert maskable["sizes"] == "512x512"
    asset = client.get(maskable["src"])
    assert asset.status_code == 200
    assert _png_dimensions(asset.data) == (512, 512)


def test_service_worker_is_root_scoped_and_not_stale_cached(client):
    response = client.get("/sw.js")
    assert response.status_code == 200
    assert response.headers.get("Service-Worker-Allowed") == "/"
    assert "no-cache" in response.headers.get("Cache-Control", "")
    assert "static/offline.html" in response.get_data(as_text=True)
    assert "obixconfigdoctor-v12-workspace" in response.get_data(as_text=True)
    assert "STATIC_ALLOWLIST" in response.get_data(as_text=True)
    assert "MAX_ASSET_BYTES" in response.get_data(as_text=True)
    assert "hero-drone-premium.webp" not in response.get_data(as_text=True)
    assert "/static/video/landing-background.mp4" not in response.get_data(as_text=True)


def test_service_worker_static_cache_is_an_explicit_bounded_allowlist():
    source = (PROJECT_ROOT / "static" / "sw.js").read_text(encoding="utf-8")
    assert "new Set(STATIC_ASSETS)" in source
    assert "if (!STATIC_ALLOWLIST.has(url.pathname) || url.search) return;" in source
    assert "const MAX_ASSET_BYTES = 512 * 1024;" in source
    assert "rawContentLength !== null" in source
    assert "contentLength !== null && contentLength <= MAX_ASSET_BYTES" in source
    assert "cache.put(request, response.clone())" in source
    assert "landing-background.mp4" not in source


def test_vercel_service_worker_mirror_matches_source():
    source = (PROJECT_ROOT / "static" / "sw.js").read_bytes()
    vercel_public = (PROJECT_ROOT / "public" / "static" / "sw.js").read_bytes()

    assert source == vercel_public


def test_workspace_styles_are_mirrored_to_vercel_public():
    for name in ("workspace-nav.css", "landing-premium.css"):
        source = (PROJECT_ROOT / "static" / "css" / name).read_bytes()
        mirror = (PROJECT_ROOT / "public" / "static" / "css" / name).read_bytes()
        assert source == mirror, name


def test_offline_fallback_is_a_static_self_contained_page(client):
    response = client.get("/static/offline.html")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "<title>ออฟไลน์ · CONFIGDOCTOR Edition</title>" in html
    assert "OBIX Config Doctor" not in html
    assert "ขณะนี้ออฟไลน์" in html
    assert "ไม่ได้ถูกเก็บไว้แบบออฟไลน์" in html
    assert "<script" not in html
    assert "https://" not in html


def test_vercel_offline_fallback_mirror_matches_source():
    source = (PROJECT_ROOT / "static" / "offline.html").read_bytes()
    vercel_public = (PROJECT_ROOT / "public" / "static" / "offline.html").read_bytes()
    assert vercel_public == source


def test_vercel_bundle_keeps_root_favicon_and_short_exclusion_pattern():
    config = json.loads((PROJECT_ROOT / "vercel.json").read_text(encoding="utf-8"))
    exclude = config["functions"]["app.py"]["excludeFiles"]
    assert len(exclude) < 256
    assert "static/favicon.png" in exclude
    assert "static/favicon.ico" not in exclude


def test_root_favicon_route_serves_real_icon(client):
    response = client.get("/favicon.ico")
    assert response.status_code == 200
    assert response.data
    assert "image" in response.mimetype
