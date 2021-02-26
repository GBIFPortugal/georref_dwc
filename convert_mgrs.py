#!/usr/bin/python -tt
#coding=utf-8

# Author: Rui Figueira
#
# File: convert_mgrs.py
# This file takes UTM coordinates in MGRS format, converts them to
# geographic decimal degree coordinates, and gets the geographic administrative
# data of the location using OpenStreeMap Nominatim Reverse API service
#
# Notes: The input is a one column csv file with  MGRS coordinates, the output
# is a csv with the same coordinates, geographic coordinates and geographic
# administrative data
#
# Created on 25-02-2021 by Rui Figueira


import mgrs
import csv
import json
import requests
from reverse_georref import getReverseGeorref

m = mgrs.MGRS()

# this file has one column with coordinates in the format 29SNDXXXX (any precision)
in_filename = "./utm_mgrs_test.csv"

out_filename = "./latlong_test.csv"


def main():
  with open(in_filename, 'r', newline='') as in_file, open(out_filename, 'w', \
  newline='') as out_file:
    file_reader = csv.reader(in_file, delimiter=',', quotechar='"', \
    quoting=csv.QUOTE_MINIMAL)
    file_writer = csv.writer(out_file, delimiter=',', quotechar="'", \
    quoting=csv.QUOTE_MINIMAL)

    # write headers in the output csv
    file_writer.writerow(["UTM, lat, long, locality, municipality, stateProvince, country, countryCode"])

    next(file_reader) #skip header row of input csv
    coordinates = ''

    result = ''

    for line in in_file:
       line = line.rstrip() #remove new line characters
       print(line)
       try:
           d = m.toLatLon(line)
           localDict = getReverseGeorref(d[0], d[1])
           result = '{},{},{},\"{}\",\"{}\",\"{}\",{},{}'.format(line, d[0], d[1], localDict["locality"], \
           localDict["municipality"], localDict["stateProvince"], localDict["country"], localDict["country_code"])
           print('result: ' + result)
       except Exception as e:
           d = "N/A"
           result = '{}|{}'.format(line, d)
           pass
       file_writer.writerow([result])


if __name__ == '__main__':
    main()
