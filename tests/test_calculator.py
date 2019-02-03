import pytest
from fee_api.calculator import FeeCalculator


@pytest.fixture
def cal():
    return FeeCalculator()


def test_get_bounds(cal):
    assert cal.get_bounds(1000, 12) == (50, 90)

    assert cal.get_bounds(18323.22, 24) == (720, 760)
    assert cal.get_bounds(1323.22, 24) == (70, 100)

    assert cal.get_bounds(20000, 12) == (400, 400)
    assert cal.get_bounds(20000, 24) == (800, 800)

    with pytest.raises(ValueError) as e:
        cal.get_bounds(20000.1, 12)
    assert str(e.value) == "loan must be 1000 <= loan <= 20000"
    with pytest.raises(ValueError) as e:
        cal.get_bounds(999.9, 12)
    assert str(e.value) == "loan must be 1000 <= loan <= 20000"
    with pytest.raises(ValueError) as e:
        cal.get_bounds(5000, 3)
    assert str(e.value) == "term must be 12 or 24"


def test_interpolate(cal):
    assert cal.interpolate(2750, 100, 120) == 115
    assert cal.interpolate(1323.22, 70, 100) == 79.6966
    assert cal.interpolate(13999, 520, 560) == 559.96
    assert cal.interpolate(14000, 560, 600) == 560

    assert cal.interpolate(1000, 50, 90) == 50
    assert cal.interpolate(1000.01, 50, 90) == 50.0004
    assert cal.interpolate(1000.10, 50, 90) == 50.004
    assert cal.interpolate(1001, 50, 90) == 50.04
    assert cal.interpolate(1010, 50, 90) == 50.4
    assert cal.interpolate(1100, 50, 90) == 54
    assert cal.interpolate(1200, 50, 90) == 58
    assert cal.interpolate(1300, 50, 90) == 62
    assert cal.interpolate(1400, 50, 90) == 66
    assert cal.interpolate(1500, 50, 90) == 70
    assert cal.interpolate(1600, 50, 90) == 74
    assert cal.interpolate(1700, 50, 90) == 78
    assert cal.interpolate(1800, 50, 90) == 82
    assert cal.interpolate(1900, 50, 90) == 86
    assert cal.interpolate(2000, 90, 90) == 90
    assert cal.interpolate(2500, 90, 90) == 90
    assert cal.interpolate(3000, 90, 115) == 90
    assert cal.interpolate(3500, 90, 115) == 102.5
    assert cal.interpolate(3999, 90, 115) == 114.975
    assert cal.interpolate(4000, 115, 100) == 115
    assert cal.interpolate(4250, 115, 100) == 111.25
    assert cal.interpolate(4500, 115, 100) == 107.5
    assert cal.interpolate(4750, 115, 100) == 103.75
    assert cal.interpolate(4999, 115, 100) == 100.015

    assert cal.interpolate(20000, 800, 800) == 800


def test_clean_fee(cal):
    assert cal.clean_fee(1000, 50) == 50
    assert cal.clean_fee(1000.01, 50.0004) == 49.99
    assert cal.clean_fee(1000.10, 50.004) == 49.9
    assert cal.clean_fee(1001, 50.04) == 49
    assert cal.clean_fee(1010, 50.4) == 50
    assert cal.clean_fee(1100, 54) == 55
    assert cal.clean_fee(1200, 58) == 60
    assert cal.clean_fee(1300, 62) == 60
    assert cal.clean_fee(1400, 66) == 65
    assert cal.clean_fee(1500, 70) == 70
    assert cal.clean_fee(1900, 86) == 85
    assert cal.clean_fee(2000, 90) == 90
    assert cal.clean_fee(2500, 90) == 90
    assert cal.clean_fee(3000, 90) == 90
    assert cal.clean_fee(3500, 102.5) == 100
    assert cal.clean_fee(3999, 114.975) == 116
    assert cal.clean_fee(4000, 115) == 115
    assert cal.clean_fee(4250, 111.25) == 110
    assert cal.clean_fee(4500, 107.5) == 110
    assert cal.clean_fee(4750, 103.75) == 105
    assert cal.clean_fee(4999, 100.015) == 101


def test_cal(cal):
    assert cal(1000, 12) == 50
    assert cal(1000.01, 12) == 49.99
    assert cal(1000.10, 12) == 49.9
    assert cal(1001, 12) == 49
    assert cal(1010, 12) == 50
    assert cal(1100, 12) == 55
    assert cal(1200, 12) == 60
    assert cal(1300, 12) == 60
    assert cal(1400, 12) == 65
    assert cal(1500, 12) == 70
    assert cal(1900, 12) == 85
    assert cal(2000, 12) == 90
    assert cal(2500, 12) == 90
    assert cal(3000, 12) == 90
    assert cal(3500, 12) == 100
    assert cal(3999, 12) == 116
    assert cal(4000, 12) == 115
    assert cal(4250, 12) == 110
    assert cal(4500, 12) == 110
    assert cal(4750, 12) == 105
    assert cal(4999, 12) == 101
    assert cal(5000, 12) == 100

    assert cal(1000, 24) == 70
    assert cal(19998, 24) == 802
    assert cal(19999, 24) == 801
    assert cal(19999.5, 24) == 800.5
    assert cal(20000, 24) == 800

    assert cal(2790.76, 24) == 114.24


def test__round(cal):
    assert cal._round(2300, 5) == 2300
    assert cal._round(2323, 5) == 2325
    assert cal._round(2322, 5) == 2320
    assert cal._round(2322.50, 5) == 2320
    assert cal._round(2322.51111, 5) == 2325
