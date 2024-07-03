#!/usr/bin/env python3
"""
Simple batch downloader for public iCloud shared albums.
"""

import argparse
import logging
import requests
import json
import sys
import os
import random
from typing import List

# Merged url_utils.py content
BASE_62_CHAR_SET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

def base62_to_int(part: str) -> int:
    """
    Simple base 62 to integer computation
    """
    t = 0
    for c in part:
        t = t * 62 + BASE_62_CHAR_SET.index(c)
    return t

def get_partition(url_token: str):
    """
    Extract partition from url token.
    (Based on JS code)
    """
    partition = 0
    if 'A' == url_token[0]:
        partition = base62_to_int([url_token[1]])
    else:
        partition = base62_to_int(url_token[1:3])
    return partition

def get_url_location(item: dict) -> str:
    """
    Extracts URL location from a given item dictionary.
    """
    return item.get('url_location')

def get_url_path(item: dict) -> str:
    """
    Extracts URL path from a given item dictionary.
    """
    return item.get('url_path')

def get_download_url(item: dict) -> str:
    """
    Constructs the full download URL from item dictionary.
    """
    url_location = get_url_location(item)
    url_path = get_url_path(item)
    return f"https://{url_location}{url_path}"

# Original iclouder.py content
def filter_best_assets(photos: List[dict], asset_urls: dict):
    """
    Makes sure to check which of the derivatives of a photo has the highest quality.
    Lower quality image downloads will be omitted.
    """
    best_checksums = []
    for photo in photos:
        maxdim = 0
        best_derivative = None
        for _, derivative in photo.get('derivatives', {}).items():
            dim = int(derivative.get('width', '0')) * int(derivative.get('height', '0'))
            if dim > maxdim:
                maxdim = dim
                best_derivative = derivative
        if best_derivative:
            best_checksums.append(best_derivative.get('checksum'))

    result = {}
    for checksum in best_checksums:
        if checksum in asset_urls:
            result[checksum] = asset_urls[checksum]
    return result

def get_stream(host: str, token: str, retries: int = 3):
    """
    Download web stream of available photos.
    """
    url = f"https://{host}/{token}/sharedstreams/webstream"
    attempt = 0
    while attempt < retries:
        try:
            response = requests.post(url, json.dumps({'streamCtag': 'null'}), allow_redirects=True)
            if response.status_code == 330:
                redirect_data = json.loads(response.content)
                new_host = redirect_data.get("X-Apple-MMe-Host")
                return get_stream(new_host, token)
            elif response.status_code == 200:
                data = json.loads(response.content)
                photos = data.get('photos')
                asset_urls = get_asset_urls(host, token, [photo['photoGuid'] for photo in photos])
                return filter_best_assets(photos, asset_urls.get('items', []))
            else:
                raise ValueError("Received an unexpected response from the server.")
        except Exception as e:
            attempt += 1
            if attempt == retries:
                raise e

def get_asset_urls(host: str, token: str, photoGuids: List[str]):
    """
    Get precise asset URLs based on a list of photo GUIDs.
    """
    url = f"https://{host}/{token}/sharedstreams/webasseturls"
    response = requests.post(url, json.dumps({'photoGuids': photoGuids}), allow_redirects=True)
    if response.status_code == 200:
        return json.loads(response.content)
    else:
        raise ValueError("Received an unexpected response from the server.")

def download_file(url: str, directory: str, filename: str = None):
    """
    Download a single photo from the given URL to the specified directory.
    """
    response = requests.get(url, allow_redirects=True)
    if response.status_code != 200:
        logger.error("Failed to download a photo.")
        logger.debug(f"Status code: {response.status_code} (for URL: {url})")
    else:
        if filename:
            output_file = os.path.join(directory, filename)
        else:
            end_index = url.index('?')
            start_index = url.rindex('/', 0, end_index)
            file_name = url[(start_index + 1):end_index]
            output_file = os.path.join(directory, file_name)
        open(output_file, 'wb').write(response.content)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("token", help="The token part of the shared iCloud album")
    parser.add_argument("--debug", help="Show logs up to the debug level.", action='store_true')
    parser.add_argument("--destination", help="Destination directory for downloaded files.", default='.')
    parser.add_argument("--single", help="Download a single random photo.", action='store_true')
    parser.add_argument("--filename", help="Filename to save the single downloaded photo as.", default='random_photo.jpg')
    arguments = parser.parse_args()

    logger = logging.getLogger("iclouder")
    logging.basicConfig(format='%(levelname)s: %(message)s',
                        level=logging.DEBUG if arguments.debug else logging.WARNING)

    logger.debug("Loading: " + arguments.token)

    partition = get_partition(arguments.token)
    logger.debug("Partition: {}".format(partition))

    host = f"p{partition}-sharedstreams.icloud.com"
    try:
        data = get_stream(host, arguments.token)
    except ValueError as e:
        logger.error("Could not retrieve item stream! (Use the debug flag for more info.)")
        if arguments.debug:
            logger.exception(e)
        sys.exit()

    directory = ""
    if not os.path.exists(arguments.destination):
        os.makedirs(arguments.destination)
    if os.path.isdir(arguments.destination):
        directory = arguments.destination
        if not directory.endswith('/'):
            directory += '/'
    elif arguments.destination != '.':
        logging.error("Destination directory does not exist!")
        sys.exit()

    if arguments.single:
        if data:
            item = random.choice(list(data.values()))
            url = get_download_url(item)
            download_file(url, directory, arguments.filename)
        else:
            logger.error("No photos available to download.")
    else:
        logger.info("Downloading: {} files.".format(len(data)))
        for key, item in data.items():
            url = get_download_url(item)
            download_file(url, directory)
