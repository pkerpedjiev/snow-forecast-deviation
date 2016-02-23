import get_forecast as gf
import sys

def test_parse_snow_amount():
    amt = gf.parse_snow_amount('-')
    assert(amt == 0)

    amt = gf.parse_snow_amount('5cm')
    assert(amt == 5)

    amt = gf.parse_snow_amount('5-10cm')
    assert((amt - 7.5) < 0.0001)

def test_parse_date():
    date = gf.parse_forecast_date('Wetterprognose 26.02.2016')

    assert(date.year == 2016)
    assert(date.month == 2)
    assert(date.day == 26)

def test_parse_forecast():
    """Parse the forecast for the test html file (Soelden)"""
    with open('test/data/soelden_wetter.html', 'r') as f:
        forecast = gf.parse_forecast(f.read())

        print >>sys.stderr, "forecast:", forecast

    pass
