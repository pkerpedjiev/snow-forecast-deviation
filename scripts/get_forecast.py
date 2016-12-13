#!/usr/bin/python

import datetime as dt
import lxml.etree as lxe
import lxml.html as lxh
import requests
import sys
import time
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
        return int(text.strip('<'))

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
    date_parts = forecast_date.split(' ')
    if len(date_parts) > 1:
        date = date_parts[1]
    else:
        date = date_parts[0]
    date = dt.datetime.strptime(date, '%d.%m.%Y')

    return date

def parse_forecast(forecast_string):
    '''
    Parse a bergfex forecast.

    :forecast_string: The text of the html page containing the forecast
    :return: A dictionary containing the current date, as well as the
             forecasts for the next few days.
    '''
    try:
        tree = lxh.fromstring(forecast_string)
    except lxe.XMLSyntaxError as xse:
        print >>sys.stderr, "XMLSyntaxError:", xse
        print >>sys.stderr, forecast_string
        return

    nine_day_forecast = tree.cssselect('.forecast9d-container')[0]
    forecasts = nine_day_forecast.cssselect('.nschnee')
    forecast_tuples = []
    for forecast in forecasts:
        snow_amount = forecast.text_content().strip()
        date = forecast.getparent().get('title').split(' ')[1]

        forecast_tuples += [(parse_forecast_date(date),
                            parse_snow_amount(snow_amount))]

    return forecast_tuples

def main():
    parser = argparse.ArgumentParser(description="""
    
    python get_forecast.py bergfex_url

    Get the bergfex snow forecast for a particular ski area.

    Output the current date as well as the date of the forecast and
    the amount of snow forecast.
""")

    parser.add_argument('url', nargs='+')
    parser.add_argument('--sleep', default=None, type=int,
                        help='Sleep before waking to get new forecast values')
    #parser.add_argument('-o', '--options', default='yo',
    #					 help="Some option", type='str')
    #parser.add_argument('-u', '--useless', action='store_true', 
    #					 help='Another useless option')

    args = parser.parse_args()

    while True:
        for url in args.url:
            try:
                page = requests.get(url)
            except requests.exceptions.ConnectionError as ce:
                print >>sys.stderr, "Connection error:", url, ce
                continue
            forecast_tuples = parse_forecast(page.content)

            current_time = dt.datetime.now();
            out_str = ''
            for forecast in forecast_tuples:
                out_str += "{}\t{}\t{}\t{}\n".format(url, dt.date.strftime(current_time, "%Y-%m-%d %H:%M"),
                                          dt.date.strftime(forecast[0], "%Y-%m-%d"),
                                          forecast[1])
            sys.stdout.write(out_str)
            sys.stdout.flush()
        print >>sys.stderr, "Got results at:", dt.date.strftime(current_time, "%Y-%m-%d %H:%M:%S")

        if args.sleep is not None:
            time.sleep(args.sleep);
        else:
            break

if __name__ == '__main__':
    main()


