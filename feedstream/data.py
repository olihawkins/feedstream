# -*- coding: utf-8 -*-

# Imports ---------------------------------------------------------------------

import datetime
import re
import feedstream.settings as settings

# Constants -------------------------------------------------------------------

TAG_RE = re.compile('<.*?>')
SPACES_RE = re.compile(' +')

# Functions -------------------------------------------------------------------

def get_datetime_from_timestamp(ts_ms):

    """Get Feedly timestamp as a datetime.datetime."""

    ts_secs = int(ts_ms / 1000)
    return datetime.datetime.fromtimestamp(ts_secs)

def get_date_from_timestamp(ts_ms):

    """Get Feedly timestamp as a date."""

    ts_secs = ts_ms / 1000
    return datetime.datetime.fromtimestamp(ts_secs).date()

def get_time_from_timestamp(ts_ms):

    """Get Feedly timestamp as a time."""

    ts_secs = ts_ms / 1000
    return datetime.datetime.fromtimestamp(ts_secs).time()

def get_iso_from_timestamp(ts_ms):

    """Get Feedly timestamp as an ISO format string."""

    ts_secs = ts_ms / 1000
    return datetime.datetime.fromtimestamp(ts_secs).isoformat()

def get_timestamp_from_datetime(dt):

    """Get Feedly timestamp from a Python datetime."""

    ts_secs = dt.timestamp()
    ts_ms = int(ts_secs * 1000)
    return ts_ms

def remove_tags(text):

    """
    Remove tags from html summaries. Tags are replaced by spaces and multiple
    spaces are replaced by a single space.
    """

    text = re.sub(TAG_RE, ' ', text)
    text = re.sub(SPACES_RE, ' ', text)
    return text.strip()

def key_exists(data_dict, *keys):

    """Test if a sequence of keys exists in a nested dictionary."""

    element = data_dict

    for key in keys:
        try:
            element = element[key]
        except KeyError:
            return False
    return True

def get_opt_key(data_dict, *keys):

    """
    Get the data for a given sequence of keys which may or may not exist in a
    nested dictionary. Returns None if the sequence of keys does not exist.
    """

    element = data_dict

    for key in keys:
        try:
            element = element[key]
        except KeyError:
            return None
    return element

def get_entry_url(entry):

    """
    Return the best available url for the entry or None if missing.
    """

    if key_exists(entry, 'canonicalUrl'):
        return entry['canonicalUrl']

    if key_exists(entry, 'canonical'):
        for c in entry['canonical']:
            if c['type'] is 'text/html':
                return c['href']

    if key_exists(entry, 'alternate'):
        for a in entry['alternate']:
            if a['type'] is 'text/html':
                return a['href']
    return None
