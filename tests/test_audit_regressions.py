import json
import math
from pathlib import Path

import pytest
from jinja2 import Environment, FileSystemLoader

from analyzer.blackbox_analyzer import _fval
from analyzer.prop_logic import analyze_propeller
from analyzer.rpm_filter_calc import calculate_rpm_filter
import core


def test_og_tags_render_when_csrf_token_is_not_available():
    template_dir = Path(__file__).resolve().parents[1] / "templates"
    env = Environment(loader=FileSystemLoader(str(template_dir)))
    env.globals.update(
        BASE_URL="https://example.test",
        url_for=lambda endpoint, **kwargs: "/static/" + kwargs.get("filename", ""),
    )
    rendered = env.get_template("partials/og_tags.html").render()
    assert 'name="csrf-token"' not in rendered
    assert "CONFIGDOCTOR Edition" in rendered


def test_html_pages_do_not_use_path_only_etags(client):
    response = client.get("/about")
    assert response.status_code == 200
    assert response.headers.get("Cache-Control") == "private, no-cache"
    assert response.headers.get("ETag") is None
    revalidated = client.get("/about", headers={"If-None-Match": '"stale-path-only-tag"'})
    assert revalidated.status_code == 200
    assert revalidated.data


@pytest.mark.parametrize("prop_size", [0, -1, float("nan"), float("inf")])
def test_validate_input_rejects_non_positive_or_non_finite_prop_size(prop_size):
    warnings = core.validate_input(5, 650, prop_size, 4.5, 3, "4S")
    assert any("prop_size" in warning or "ใบพัด" in warning for warning in warnings)


@pytest.mark.parametrize("prop_size", [0, -1, float("nan"), float("inf")])
def test_propeller_calculator_rejects_invalid_diameter(prop_size):
    with pytest.raises(ValueError, match="prop_size"):
        analyze_propeller(prop_size, 4.3, 3, "freestyle")


def test_propeller_calculator_rejects_invalid_pitch():
    with pytest.raises(ValueError, match="prop_pitch"):
        analyze_propeller(5, float("nan"), 3, "freestyle")


@pytest.mark.parametrize("value", ["NaN", "Infinity", "-Infinity"])
def test_blackbox_numeric_parser_never_returns_non_finite_values(value):
    parsed = _fval({"signal": value}, "signal", default=0.0)
    assert math.isfinite(parsed)
    assert parsed == 0.0


@pytest.mark.parametrize("csv_value", [123, [], {}, None])
def test_blackbox_api_rejects_non_string_csv_payload(client, csv_value):
    response = client.post(
        "/blackbox/analyze",
        data=json.dumps({"csv": csv_value}),
        content_type="application/json",
    )
    assert response.status_code == 400
    assert response.json["error"] == "csv must be a string"


@pytest.mark.parametrize("kv", [0, -1, float("nan"), float("inf"), 2300.5, "not-a-number"])
def test_rpm_calculator_rejects_invalid_kv(kv):
    with pytest.raises(ValueError, match="kv"):
        calculate_rpm_filter(kv, "4S", 5)


@pytest.mark.parametrize("prop_size", [0, -1, float("nan"), float("inf")])
def test_rpm_calculator_rejects_invalid_prop_size(prop_size):
    with pytest.raises(ValueError, match="prop_size"):
        calculate_rpm_filter(2300, "4S", prop_size)


def test_community_rating_and_like_endpoints_handle_duplicate_submissions(client, monkeypatch, tmp_path):
    monkeypatch.setattr(core, "_DB_PATH", str(tmp_path / "community.db"))
    bad_rating = client.post("/api/rating", json={"stars": 0})
    assert bad_rating.status_code == 400
    rating = client.post("/api/rating", json={"stars": 5})
    assert rating.status_code == 200
    assert rating.json["ok"] is True
    duplicate_rating = client.post("/api/rating", json={"stars": 4})
    assert duplicate_rating.status_code == 409
    like = client.post("/api/like", json={})
    assert like.status_code == 200
    duplicate_like = client.post("/api/like", json={})
    assert duplicate_like.status_code == 409


def test_main_analysis_warns_and_avoids_invalid_propeller_math(client):
    payload = {
        "size": "5", "weight": "650", "prop_size": "-1", "pitch": "4.5",
        "blades": "3", "battery": "4S", "style": "freestyle", "motor_kv": "2400",
    }
    with client.application.test_request_context("/app", method="POST", data=payload):
        analysis = core._handle_analysis_post()
    assert any(
        "ขนาดใบพัดต้องมากกว่า 0 นิ้ว" in warning.get("msg", "")
        for warning in analysis["warnings"]
    )
    assert analysis["prop_result"]["summary"] == "prop analysis not available"
    assert "tip_speed_mps" not in analysis["prop_result"]["effect"]
