import pytest
from main import CPE_2_3

@pytest.fixture
def valid_cpe():
    return "cpe:2.3:a:microsoft:internet_explorer:8.0.6001:beta:*:en-US:*:*:*:*"


@pytest.fixture
def expected_result():
    return {
        "part": "a",
        "vendor": "microsoft",
        "product": "internet_explorer",
        "version": "8.0.6001",
        "update": "beta",
        "edition": "ANY",
        "language": "en-US",
        "sw_edition": "ANY",
        "target_sw": "ANY",
        "target_hw": "ANY",
        "other": "ANY"
    }

def test_parse_cpe_valid(valid_cpe, expected_result):
    parsed_result = CPE_2_3().parse_cpe(valid_cpe)

    assert isinstance(parsed_result, dict)
    assert parsed_result == expected_result

@pytest.mark.parametrize("invalid_cpe", [
    "cpe:2.3:invalid_format",
    "cpe:2.3:a:micr:osoft:internet_explorer:8.0.6001:beta:*:*:*:*:*:*",
    "cpe:2.3:a::internet_explorer:8.0.6001:beta:*:*:*:*:*:*",
    "cpe:2.3:a:microsoft:internet_explorer:8.0.6001:beta:*:*:*:*:*:*:*",
    ":a:microsoft:internet_explorer:8.0.6001:beta:*:*:*:*:*:*",
    "cpe:2.3:a:microsoft:intern et_explorer:8.0.6001:beta:*:*:*:*:*:*",
    "cpe:2.3:a:microsoft::8.0.6001:beta:*:*:*:*:*:*",
    "cpe:2.3:a:microsoft:internet_explorer:8.0.6001:beta:*:12-US:*:*:*:*",
    "cpe:2.3:a:microsoft:internet_explorer:8.0.6001::*:en-US:*:*:*:*",
    "cpe:2.3:a:microsoft::8.0.6001:beta:*:en-US:*:*:*:*",
    "cpe:2.3:a:microsoft:internet_explorer::beta:*:en-US:*:*:*:*",
    "cpe:2.3:a:microsoft:internet_explorer:8.0.6001::*:en-US:*:*:*:*"
])
def test_parse_cpe_invalid(invalid_cpe):
    with pytest.raises(Exception):
        CPE_2_3().parse_cpe(invalid_cpe)
