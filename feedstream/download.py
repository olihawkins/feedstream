# -*- coding: utf-8 -*-

# Imports ---------------------------------------------------------------------

import csv
import datetime
import os
import pathlib
import feedstream.fetch as fetch
import feedstream.data as data
from feedstream.config import settings

# Constants -------------------------------------------------------------------

TIMESTAMP_FILE = os.path.join(settings.timestamp_file)

# Download functions ----------------------------------------------------------

def download_entries():

    """Download entries from each tag to a csv."""

    items = []
    since = get_last_downloaded() if settings.download_new else None
    downloaded = data.get_timestamp_from_datetime(datetime.datetime.now())
    tag_ids = fetch.fetch_tag_ids()

    for tag_id in tag_ids:

        continuation = None

        while True:

            contents = fetch.fetch_tag_entries(tag_id['id'],
                since=since, continuation=continuation)

            for item in contents['items']:

                item = data.parse_entry(tag_id['id'], tag_id['label'], item)
                items.append(item)

            continuation = data.get_opt_key(contents, 'continuation')
            if continuation is None:
                break

    entries = {
        'downloaded': downloaded,
        'fieldnames': data.FIELDNAMES,
        'items': items}

    return entries

# Save data functions ---------------------------------------------------------

def write_entries_csv(entries):

    """Write entries to a csv."""

    downloaded = entries['downloaded']
    fieldnames = entries['fieldnames']
    items = entries['items']

    try:

        pathlib.Path(settings.data_dir).mkdir(exist_ok=True)

        filename = '{0}-{1}-{2}.csv'.format(
            settings.download_prefix,
            data.get_date_from_timestamp(downloaded),
            data.get_time_from_timestamp(downloaded).strftime('%H-%M-%S'))

        filepath = os.path.join(settings.data_dir, filename)

        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames,
                quoting=csv.QUOTE_NONNUMERIC)
            writer.writeheader()
            for item in items:
                writer.writerow(item)

        set_last_downloaded(downloaded)
        return filename

    except:
        raise

# Timestamp functions ---------------------------------------------------------

def get_last_downloaded():

    """Get the timestamp for the last time data was downloaded."""

    try:
        with open(TIMESTAMP_FILE) as f:
            timestamp_str = f.read()
            return int(timestamp_str)
    except FileNotFoundError:
        return None


def set_last_downloaded(timestamp):

    """Set the timestamp for the last time data was downloaded."""

    pathlib.Path(settings.data_dir).mkdir(exist_ok=True)

    with open(TIMESTAMP_FILE, 'w') as f:
        f.write('{0}'.format(timestamp))
