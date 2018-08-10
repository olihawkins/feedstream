# -*- coding: utf-8 -*-

# Imports ---------------------------------------------------------------------

import datetime
import html
import pytz
import re
import feedstream.settings as settings

# Constants -------------------------------------------------------------------

RE_TAG = re.compile(r'<[^>]+?>')
RE_WHITESPACE = re.compile('\s+')
RE_WHITESPACE_PUNCTUATION = re.compile(r'\s([?,;:.)}\]"](?:\s|$))')
RE_WHITESPACE_EXCLAMATION = re.compile(r'\s(!+(?:\s|$))')
RE_END_CONTINUE = re.compile(' Continue reading\.\.\.\s*$')
RE_END_DOTS = re.compile('\.\.\.\s*$')
TRUNCATE_LENGTH = 300
TRUNCATE_MARKER = '...'
TIMEZONE = pytz.timezone(settings.timezone)
SEPARATOR = '<sep>'
FIELDNAMES = [
    'tag_id',
    'tag_label',
    'add_timestamp',
    'add_date',
    'add_time',
    'pub_date',
    'publisher',
    'url',
    'title',
    'author',
    'summary',
    'keywords',
    'comments',
    'highlights',
    'article_id']

# Functions -------------------------------------------------------------------

def get_datetime_from_timestamp(ts_ms, tz=TIMEZONE):

    """Get Feedly timestamp as a datetime.datetime."""

    ts_secs = int(ts_ms / 1000)
    return datetime.datetime.fromtimestamp(ts_secs, tz=tz)


def get_date_from_timestamp(ts_ms, tz=TIMEZONE):

    """Get Feedly timestamp as a date."""

    ts_secs = ts_ms / 1000
    return datetime.datetime.fromtimestamp(ts_secs, tz=tz).date()


def get_time_from_timestamp(ts_ms, tz=TIMEZONE):

    """Get Feedly timestamp as a time."""

    ts_secs = ts_ms / 1000
    return datetime.datetime.fromtimestamp(ts_secs, tz=tz).time()


def get_iso_from_timestamp(ts_ms, tz=TIMEZONE):

    """Get Feedly timestamp as an ISO format string."""

    ts_secs = ts_ms / 1000
    return datetime.datetime.fromtimestamp(ts_secs, tz=tz).isoformat()


def get_timestamp_from_datetime(dt):

    """Get Feedly timestamp from a Python datetime."""

    ts_secs = dt.timestamp()
    ts_ms = int(ts_secs * 1000)
    return ts_ms


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

    """Return the best available url for the entry or None if missing."""

    if key_exists(entry, 'canonicalUrl'):
        return entry['canonicalUrl']

    if key_exists(entry, 'canonical'):
        for c in entry['canonical']:
            if key_exists(c, 'href'):
                return c['href']

    if key_exists(entry, 'alternate'):
        for a in entry['alternate']:
            if key_exists(a, 'href'):
                return a['href']

    return None


def clean_text(text):

    """
    Cleans html text. Removes tags from html summaries. Tags are replaced by
    spaces and then multiple whitespace characters are replaced by a single
    space. Whitespace before puncuation is then removed, followed by any
    continue reading markers. Any leading or trailing whitespace is stripped.

    """

    text = html.unescape(text)
    text = re.sub(RE_TAG, ' ', text)
    text = re.sub(RE_WHITESPACE, ' ', text)
    text = re.sub(RE_WHITESPACE_PUNCTUATION, r'\1', text)
    text = re.sub(RE_WHITESPACE_EXCLAMATION, r'\1', text)
    text = re.sub(RE_END_CONTINUE, '', text)
    text = re.sub(RE_END_DOTS, '', text)

    return text.strip()


def truncate(text, length=TRUNCATE_LENGTH, marker=None):

    """
    Truncate the text to the given length, rounded to the last full word.
    If a truncation marker is set, add a space to the string followed by
    the given truncation marker.

    """

    if len(text) > length:
        end = text[:length].rfind(' ')
        text = text[:end]
        if marker is not None:
            text = '{0} {1}'.format(text, marker)
    return text


def parse_entry(tag_id, tag_label, item):

    """
    Parse an entry item returned from the API, simplify and clean the data,
    and return it as a flat dictionary.

    """

    entry = {}
    entry['tag_id'] = tag_id
    entry['tag_label'] = clean_text(tag_label)
    entry['article_id'] = item['id']
    entry['url'] = get_entry_url(item)

    # Handle title
    entry['title'] = get_opt_key(item, 'title')
    if entry['title'] is not None:
        entry['title'] = clean_text(entry['title'])

    # Handle author
    entry['author'] = get_opt_key(item, 'author')
    if entry['author'] is not None:
        entry['author'] = clean_text(entry['author'])

    # Handle publisher
    entry['publisher'] = get_opt_key(item, 'origin', 'title')
    if entry['publisher'] is not None:
        entry['publisher'] = clean_text(entry['publisher'])

    # Handle add date
    add_date = get_opt_key(item, 'actionTimestamp')

    if add_date is not None:
        entry['add_timestamp'] = item['actionTimestamp']
        entry['add_date'] = get_date_from_timestamp(add_date)
        entry['add_time'] = get_time_from_timestamp(
            add_date).strftime('%H:%M:%S')
    else:
        entry['add_timestamp'] = None
        entry['add_date'] = None
        entry['add_time'] = None

    # Handle pub date
    pub_date = get_opt_key(item, 'published')

    if pub_date is not None:
        entry['pub_date'] = get_date_from_timestamp(pub_date)
    else:
        entry['pub_date'] = None

    # Handle summary text
    summary = get_opt_key(item, 'summary', 'content')

    if summary is not None:
        entry['summary'] = clean_text(summary)
    else:
        full_content = get_opt_key(item, 'fullContent')
        if full_content is not None:
            entry['summary'] = truncate(clean_text(full_content))
        else:
            entry['summary'] = None

    # Handle keywords
    keywords = get_opt_key(item, 'keywords')
    if keywords is not None:
        words = []
        for keyword in keywords:
            words.append(clean_text(keyword))
        entry['keywords'] = SEPARATOR.join(words)
    else:
        entry['keywords'] = None

    # Handle annotations, which are comments and highlights
    annotations = get_opt_key(item, 'annotations')

    if annotations is not None:

        comments = []
        highlights = []

        for annotation in annotations:

            comment = get_opt_key(annotation, 'comment')
            if comment is not None:
                comments.append(clean_text(comment))

            highlight = get_opt_key(annotation, 'highlight')
            if highlight is not None and 'text' in highlight:
                highlights.append(clean_text(highlight['text']))

        if len(comments) > 0:
            entry['comments'] = SEPARATOR.join(comments)
        else:
            entry['comments'] = None

        if len(highlights) > 0:
            entry['highlights'] = SEPARATOR.join(highlights)
        else:
            entry['highlights'] = None

    else:
        entry['comments'] = None
        entry['highlights'] = None

    return entry
