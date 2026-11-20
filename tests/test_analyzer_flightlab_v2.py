from pathlib import Path


def test_flightlab_v2_assets_are_linked_and_mirrored(client):
    root = Path(__file__).resolve().parents[1]
    html = client.get('/app').get_data(as_text=True)

    assert 'css/analyzer-flightlab-v2.css' in html
    assert 'js/analyzer-flightlab-v2.js' in html
    assert 'FPV Flight Lab' in html
    assert 'flightlab-form-status' in html
    assert 'flightlabFrame' in html

    css = client.get('/static/css/analyzer-flightlab-v2.css')
    js = client.get('/static/js/analyzer-flightlab-v2.js')
    assert css.status_code == 200
    assert js.status_code == 200
    assert css.data == (root / 'public/static/css/analyzer-flightlab-v2.css').read_bytes()
    assert js.data == (root / 'public/static/js/analyzer-flightlab-v2.js').read_bytes()


def test_flightlab_v2_preserves_analysis_controls_and_original_workbench(client):
    html = client.get('/app').get_data(as_text=True)

    for item in (
        'id="aForm"', 'id="fSz"', 'id="fWtV"', 'id="fPrV"',
        'id="battSel"', 'id="fSt"', 'id="fKv"', 'id="btnA"',
        'id="analyzer-setup"', 'id="analyzer-results"',
        'name="csrf_token"', 'id="analyzerMobileSubmit"',
    ):
        assert item in html

    js = (Path(__file__).resolve().parents[1] / 'static/js/analyzer-flightlab-v2.js').read_text()
    assert 'updateSnapshot' in js
    assert 'localStorage' in js


def test_flightlab_v2_analysis_sections_render_with_real_analysis(client):
    payload = {
        'size': '5', 'battery': '4S', 'style': 'freestyle', 'weight': '700',
        'prop_size': '5.1', 'blades': '3', 'pitch': '4.3', 'motor_kv': '2306',
        'battery_mAh': '1500', 'motor_count': '4', 'bf_version': '4.4',
    }
    response = client.post('/app', data=payload)
    assert response.status_code == 200
    html = response.get_data(as_text=True)

    assert 'data-mobile-view="results"' in html
    assert 'อ่านค่าจาก Flight Model' in html
    assert 'POWER &amp; BATTERY' in html or 'POWER & BATTERY' in html
    assert 'PROP PHYSICS' in html
    assert 'Tuning Notes สำหรับ Build นี้' in html
    assert 'First Flight Ritual' in html
    assert 'flightlabCheckCount' in html
    assert 'data-flight-check' in html
    assert 'สูตรคำนวณ' not in html or 'คำอธิบายวิธีคำนวณ' in html
    assert '{{ _twr' not in html
