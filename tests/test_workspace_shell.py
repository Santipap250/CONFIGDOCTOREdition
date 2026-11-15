from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_fpv_hub_renders_shared_workspace_shell_and_pwa(client):
    response = client.get("/fpv")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert 'href="/static/css/workspace-nav.css"' in html
    assert 'class="workspace-header"' in html
    assert 'class="bnav"' in html
    assert 'data-workspace-tab="home"' in html
    assert 'data-workspace-tab="tools"' in html
    assert 'data-workspace-tab="analyze"' in html
    assert 'data-workspace-tab="saved"' in html
    assert 'data-workspace-tab="more"' in html
    assert 'data-workspace-tab="more"' in html and 'aria-current="page"' in html
    assert 'rel="manifest" href="/manifest.json"' in html
    assert "navigator.serviceWorker.register('/sw.js'" in html
    assert "data-theme-toggle" in html and "data-language-toggle" in html
    assert 'href="/fpv-trainer"' in html and 'href="/fpv-gear"' in html


def test_landing_fragment_updates_desktop_section_and_mobile_tab_states():
    nav = (ROOT / "templates" / "partials" / "bottom_nav.html").read_text(encoding="utf-8")
    assert "[data-workspace-tab]" in nav
    assert '.cd-top-nav a[href^="#"]' in nav
    assert "'#tools':'tools','#saved':'saved','#resources':'more'" in nav
    assert "setAttribute('aria-current', 'location')" in nav
    assert "window.addEventListener('hashchange', syncWorkspaceTab)" in nav


def test_fpv_grid_can_shrink_below_280px_at_320px_viewport():
    template = (ROOT / "templates" / "fpv" / "index.html").read_text(encoding="utf-8")
    assert "minmax(min(280px, 100%), 1fr)" in template
    assert 'filename=\'css/workspace-nav.css\'' in template
