from pathlib import Path


def test_analyzer_workbench_assets_are_served_and_mirrored(client):
    root = Path(__file__).resolve().parents[1]
    html = client.get('/app').get_data(as_text=True)

    assert 'css/analyzer-workbench.css' in html
    assert 'js/analyzer-workbench.js' in html
    assert 'id="analyzer-setup"' in html
    assert 'id="analyzer-results"' in html
    assert 'data-mobile-view="setup"' in html

    css = client.get('/static/css/analyzer-workbench.css')
    js = client.get('/static/js/analyzer-workbench.js')
    assert css.status_code == 200
    assert js.status_code == 200
    assert css.data == (root / 'public/static/css/analyzer-workbench.css').read_bytes()
    assert js.data == (root / 'public/static/js/analyzer-workbench.js').read_bytes()


def test_analyzer_mobile_workbench_keeps_original_form_controls(client):
    html = client.get('/app').get_data(as_text=True)
    for item in (
        'id="aForm"', 'id="fSz"', 'id="fWtV"', 'id="fPrV"',
        'id="battSel"', 'id="fSt"', 'id="fKv"', 'id="btnA"',
        'name="csrf_token"', 'window.onAnalyzeSubmit=function(form)',
    ):
        assert item in html

    js_source = (Path(__file__).resolve().parents[1] / 'static/js/analyzer-workbench.js').read_text()
    assert 'requestSubmit()' in js_source
    assert 'setSz(this)' in html
    assert 'setBatt(' in html
    assert 'setStyle(' in html


def test_analyzer_mobile_results_tab_is_selected_after_analysis(client):
    payload = {
        'size': '5', 'battery': '4S', 'style': 'freestyle', 'weight': '700',
        'prop_size': '5.1', 'blades': '3', 'pitch': '4.3', 'motor_kv': '2306',
        'battery_mAh': '1500', 'motor_count': '4',
    }
    response = client.post('/app', data=payload)
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert 'data-mobile-view="results"' in html
    assert 'aria-selected="true"\n          data-analyzer-view="results"' in html
    assert 'id="fullcli"' in html
    assert 'id="sharePanel"' in html
