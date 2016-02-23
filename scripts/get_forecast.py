#!/usr/bin/python

import datetime as dt
import lxml.html as lxh
import requests
import sys
import argparse

def parse_snow_amount(snow_forecast_text):
    '''
    Parse snow forecast text and turn it into a number.

    I.e:
        -       =>     0
        5cm     =>     5
        5-10cm  =>     7.5

    :param snow_forecast_text: A particular day's snow forecast from bergfex.
    :return: A number from the text
    '''
    # strip cm from the text
    text = snow_forecast_text.strip()
    if text == '-':
        return 0

    text = text.strip('cm')
    if text.find('-') < 0:
        return int(text)

    parts = text.split('-')
    return (float(parts[1]) - float(parts[0])) / 2

def parse_forecast_date(forecast_date):
    '''
    Parse the forecast date:

    I.e:
        Wetterprognose 26.02.2016 => [datetime object]
    :param forecast_date: A forecast date string
    :return: A python datetime object
    '''
    date = forecast_date.split(' ')[1]
    print >>sys.stderr, "date:", date
    date = dt.datetime.strptime(date, '%d.%m.%Y')

    return date

def parse_forecast(forecast_string):
    '''
    Parse a bergfex forecast.

    :forecast_string: The text of the html page containing the forecast
    :return: A dictionary containing the current date, as well as the
             forecasts for the next few days.
    '''
    tree = lxh.fromstring(forecast_string)

    nine_day_forecast = tree.cssselect('.forecast9d-container')[0]
    forecasts = nine_day_forecast.cssselect('.nschnee')
    for forecast in forecasts:
        snow_amount = forecast.text_content().strip()
        date = forecast.getparent().get('title').split(' ')[1]
        print >>sys.stderr, snow_amount, date

        
    #print >>sys.stderr, "forecasts:", forecasts

    return None

def main():
    parser = argparse.ArgumentParser(description="""
    
    python get_forecast.py bergfex_url

    Get the bergfex snow forecast for a particular ski area.

    Output the current date as well as the date of the forecast and
    the amount of snow forecast.
""")

    #parser.add_argument('argument', nargs=1)
    #parser.add_argument('-o', '--options', default='yo',
    #					 help="Some option", type='str')
    #parser.add_argument('-u', '--useless', action='store_true', 
    #					 help='Another useless option')

    args = parser.parse_args()
    print "args:", args


if __name__ == '__main__':
    main()


