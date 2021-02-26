#!/usr/bin/python -tt
#coding=utf-8

# Author: Rui Figueira
#
# File: reverse_georref.py
# This file takes geographic coordinates in decimal formal and makes a reverse
# georreferencing on OpenStreetMap to returns an object with the values for
# the following Darin Core terms: locality, municipality, stateProvince, country
# and countryCode.
#
# Note: The reverse georreferencing was customised for the geographic context of Portugal,
# in which we use the term stateProvince to report districts.
#
# Created on 25-02-2021 by Rui Figueira


import json
import requests
import argparse



def getReverseGeorref(lat, long):
    address = 'https://nominatim.openstreetmap.org/reverse.php?lat={}&lon={}\
&zoom=10&format=jsonv2'.format(lat, long)

    try:
        txt = requests.get(address)
    except IOError:
        print('problema no acesso ao openstreetmap: código:', txt.raise_for_status())
    parsed_json = json.loads(txt.text)

    name = parsed_json.get('name')
    display_name = parsed_json.get('display_name')
    municipality = parsed_json['address'].get('municipality')
    town = parsed_json['address'].get('town')
    county = parsed_json['address'].get('county')
    country = parsed_json['address'].get('country')
    country_code = parsed_json['address'].get('country_code')

    # openstreetmap not always has the same administrative levels available
    # on town/municipality level. It is needed to find which is one is available
    # and use it\

    if municipality == None and town != None:
        municipality = town

    prev = display_name.split(municipality)
    local = prev[0]
    if (len(local) == 0):
        local = municipality

    local = local.rstrip()
    local = local.rstrip(',')

    if municipality == None:
        municipality = ''

    if county == None:
        county = ''

    result = {"locality": local, "municipality": municipality, "stateProvince": county, "country": country,\
    "country_code": country_code}
    return(result)


def main():
    parser = argparse.ArgumentParser(description = "Ajuda para o uso deste script.")
    parser.add_argument("-l", "--latlong", help = "Coordenadas no formato graus, \
    pela seguinte ordem: latitude longitude. Exemplo: 39.23932 -8.32421", required = False, default = "39.23932 -8.32421")

    argument = parser.parse_args()
    arg_latlong = argument.latlong
    latlong = arg_latlong.split(" ")
    result = getReverseGeorref(latlong[0], latlong[1])
    print(result)



if __name__ == '__main__':
    main()
