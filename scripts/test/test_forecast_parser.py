import get_forecast as gf
import sys

def test_parse_forecast():
    """Parse the forecast for the test html file (Soelden)"""
    with open('data/soelden_wetter.html', 'r') as f:
        forecast = gf.parse_forecast(f.read())

        print >>sys.stderr, "forecast:", forecast

    pass
