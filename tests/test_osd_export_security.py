def test_osd_cli_export_escapes_controls_and_sanitizes_type(client):
    response = client.post(
        "/osd/export?format=cli",
        json={
            "items": [
                {
                    "type": "GPS\nset motor_pwm_protocol = PWM",
                    "label": 'HUD"\nset p_roll = 999',
                    "x": "nan",
                    "y": "-inf",
                    "size": "10001",
                }
            ]
        },
    )

    assert response.status_code == 200
    lines = response.get_data(as_text=True).splitlines()
    assert len(lines) == 3  # header plus two comments; untrusted newlines stay on one line
    assert lines[1].startswith('// 1. unknown ')
    assert not any(line.lstrip().startswith("set ") for line in lines)
    assert '\\"' in lines[1]  # embedded quotes are escaped in the CLI text
    assert "@0,0 size=0" in lines[1]


def test_osd_cli_export_handles_wrong_items_shape(client):
    response = client.post("/osd/export?format=cli", json={"items": {"bad": "shape"}})
    assert response.status_code == 200
    assert response.get_data(as_text=True).splitlines() == ["# OBIXConfig pseudo CLI export"]
