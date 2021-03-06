import os

import json
import requests

from django.conf import settings
from django.contrib.gis.utils import LayerMapping
from models import LotProfile, Neighborhood

dor_parcel_mapping = {
    'basereg' : 'BASEREG',
}

pwd_parcel_mapping = {
    'opa_code': 'TENCODE', 
    'address': 'ADDRESS',
    'pwd_parcel': 'MULTIPOLYGON'
}

neighborhood_mapping = {
    'name': 'NAME',
    'map_name': 'MAPNAME',
    'list_name': 'LISTNAME',
    'bounds': 'MULTIPOLYGON'
}

neighborhoods = 'Neighborhoods_Philadelphia/neighborhoods_philadelphia.shp'
point_breeze = 'point_breeze/point_breeze_pwd_parcels.shp'
tioga = 'tioga/tioga_pwd_parcels.shp'
maguire = 'maguire/maguire_pwd_parcels.shp'
nicetown = 'nicetown/nicetown_pwd_parcels.shp'
old_kensington = 'old_kensington/old_kensington_pwd_parcels.shp'
upper_kensington = 'upper_kensington/upper_kensington_pwd_parcels.shp'
west_kensington = 'west_kensington/west_kensington_pwd_parcels.shp'
east_kensington = 'east_kensington/east_kensington_pwd_parcels.shp'
fairhill = 'fairhill/fairhill_pwd_parcels.shp'
brewerytown = 'brewerytown/brewerytown_pwd_parcels.shp'
hunting_park = 'hunting_park/hunting_park_pwd_parcels.shp'
harrowgate = 'harrowgate/harrowgate_pwd_parcels.shp'
strawberry_mansion = 'strawberry_mansion/strawberry_mansion_pwd_parcels.shp'


def _get_filepath(file):
    return os.path.abspath(os.path.join(settings.PROJECT_ROOT, 'data', file))

def map(model, file, mapping, verbose=True, strict=True, progress=False, step=False):
    data_source = _get_filepath(file)
    lm = LayerMapping(model, data_source, mapping,
                      transform=False, encoding='iso-8859-1')
    lm.save(verbose=verbose, strict=strict, progress=progress, step=step)

def load_addresses(start=0):
    stop = start+1000
    url = settings.PHL_DATA["ADDRESSES"] + "query"
    params = {"where":"OBJECTID > %s AND OBJECTID < %s" % (start, stop),
              "returnGeometry":"true",
              "outSR":"4326",
              "outFields":"ADDRESS, TENCODE, BRT_ID", 
              "f":"json"}

    data = requests.get(url, params=params)

    lots = json.loads(data.text)[features]





