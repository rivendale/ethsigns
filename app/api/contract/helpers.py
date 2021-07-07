import os
import calendar
import requests
import json
import tempfile
from config import AppConfig
from flask_restplus import marshal

from ..models.signs import DaySign, MonthSign, Zodiacs
from ..schema import signs_schema
basedir = os.path.abspath(os.path.dirname(__file__))


def create_nft(nft_metadata):
    del nft_metadata['image_url']
    del nft_metadata['minted']
    del nft_metadata['hash']
    del nft_metadata['minting_fee']
    del nft_metadata['id']
    del nft_metadata['month_animal']['id']
    del nft_metadata['day_animal']['id']
    temp_file = tempfile.NamedTemporaryFile(mode="w+")
    json.dump(nft_metadata, temp_file)
    temp_file.flush()

    asset_name = nft_metadata['name'].lower()

    image_data = open(os.path.join(basedir, f'../../static/{asset_name}.png'), 'rb')
    jsonfile = open(temp_file.name, 'r')
    files = [
        ('file', (f"{asset_name}.png", image_data, 'image/png')),
        ('file', ("metadata.json", jsonfile, 'application/json'))
    ]

    headers = {
        "Authorization": f"Bearer {AppConfig.IPFS_API_KEY}"
    }
    cid = ""
    try:
        resp = requests.post(AppConfig.IPFS_URL, files=files, headers=headers)
        if resp.status_code == 200:
            data = resp.json()
            cid = data['value']['cid']
    except Exception as e:
        print(e)

    return cid


def ensure_ipfs_uri_prefix(cid_or_uri):
    uri = cid_or_uri
    if not uri.startswith('ipfs://'):
        uri = 'ipfs://' + cid_or_uri

    if uri.startswith('ipfs://ipfs/'):
        uri = uri.replace('ipfs://ipfs/', 'ipfs://')

    return uri


def strip_ipfs_uri_prefix(cid_or_uri):
    if cid_or_uri.startswith('ipfs://'):
        return cid_or_uri.strip("ipfs://")

    return cid_or_uri


def make_gateway_url(ipfs_uri):
    return AppConfig.IPFS_GATEWAY_URL + '/' + strip_ipfs_uri_prefix(ipfs_uri)


def format_sign(data):
    year = data.get("year", '')
    month = data.get("month", '')
    day = data.get("day", '')
    month = MonthSign.query.filter_by(month=month).first()
    base_year = 1948
    base_index = (year-base_year) % 12
    sign = Zodiacs.query.filter_by(
        base_index=base_index).first()
    day = DaySign.query.filter_by(day=calendar.day_name[day]).first()
    setattr(sign, "month", month)
    setattr(sign, "day", day)

    resp = marshal(sign, signs_schema)
    return resp
