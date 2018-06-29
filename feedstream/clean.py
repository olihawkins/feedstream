# -*- coding: utf-8 -*-

# Imports ---------------------------------------------------------------------

import datetime
import re

TAG_RE = re.compile('<.*?>')
SPACES_RE = re.compile(' +')

# Functions -------------------------------------------------------------------

def get_timestamp_dt(timestamp):

    """Get Feedly timestamp as datetime.datetime."""

    secs = timestamp / 1000
    return datetime.datetime.fromtimestamp(secs)

def get_timestamp_iso(timestamp):

    """Get Feedly timestamp as ISO format string."""

    secs = timestamp / 1000
    return datetime.datetime.fromtimestamp(secs).isoformat()

def get_timestamp_date(timestamp):

    """Get Feedly timestamp as ISO format string."""

    secs = timestamp / 1000
    return datetime.datetime.fromtimestamp(secs).date()

def get_timestamp_time(timestamp):

    """Get Feedly timestamp as ISO format string."""

    secs = timestamp / 1000
    return datetime.datetime.fromtimestamp(secs).time().strftime('%H:%M:%S')

def remove_tags(text):

    """
    Remove tags from html summaries. Tags are replaced by spaces and multiple
    spaces are replaced by a single space.
    """

    text = re.sub(TAG_RE, ' ', text)
    text = re.sub(SPACES_RE, ' ', text)
    return text.strip()

def key_exists(data_dict, *keys):

    """Test if a sequence of nested keys exists in a dictionary."""

    element = data_dict

    for key in keys:
        try:
            element = element[key]
        except KeyError:
            return False
    return True

def get_optional_key(data_dict, *keys):

    """
    Get data for a sequence of keys in a dictionary or return None if the
    sequence of keys does not exist.
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
