#!/usr/bin/python

import lxml
import requests
import sys
import argparse

def parse_forecast(forecast_string):
    '''
    Parse a bergfex forecast.

    :forecast_string: The text of the html page containing the forecast
    :return: A dictionary containing the current date, as well as the
             forecasts for the next few days.
    '''
    tree = lxml.html.fromstring(forecast_string)

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


