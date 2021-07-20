import secrets
import string
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

headers = {
    "Authorization": f"Bearer {AppConfig.IPFS_API_KEY}"
}


def generate_random_seed(size=45):
    string.punctuation = '().-'
    return ''.join(secrets.choice(
        string.ascii_uppercase + string.ascii_lowercase +
        string.punctuation + string.digits)
        for i in range(size))


def get_nft_data(cid):
    nft = []
    try:
        response = requests.get(f"{AppConfig.IPFS_URL}/{cid}", headers=headers)
        if response.status_code == 200:
            files = response.json()['value']['files']
            nft.append(files[0]['name'])
            nft.append(files[1]['name'])
        else:
            print(response.content, cid)
    except Exception as e:
        print(e)
    return nft


def create_nft(nft_metadata):
    del nft_metadata['image_url']
    del nft_metadata['minted']
    del nft_metadata['hash']
    del nft_metadata['minting_fee']
    nft_metadata['id'] = generate_random_seed()
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

    cid = ""
    try:
        resp = requests.post(f"{AppConfig.IPFS_URL}/upload", files=files, headers=headers)
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


def make_gateway_url(ipfs_uri, metadata=None):
    url = AppConfig.IPFS_GATEWAY_URL + '/' + strip_ipfs_uri_prefix(ipfs_uri)
    if metadata:
        urls = {
            "image_url": f"{url}/{metadata[0]}",
            "metadata_url": f"{url}/{metadata[1]}"
        }
        try:
            metadata = requests.get(urls['metadata_url']).json()
            urls['token_metadata'] = metadata
        except Exception as e:
            print(e)
        return urls
    return url


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
