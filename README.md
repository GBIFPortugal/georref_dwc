# georref_dwc
Tools to help convert coordinates and obtain geographic data, in accordance with the Darwin Core standard.

This repo contains scripts to help preparing a data table of species occurrences with the geographic information in Darwin Core standard format.

The operations that can be performed are:
- to convert UTM Military Grid Reference System (MGRS) coordinates in geographic coordinates: script `convert_mgrs`
- to get geographic information for a location from a reverse georreferencing operation using the [OpenStreetMap Nominatim](https://nominatim.openstreetmap.org/ui/reverse.html) API: script `reverse_georref.py`.
`utm_mgrs_test` and `latlong_test.csv` are sample input and output files.
