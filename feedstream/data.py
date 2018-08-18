# -*- coding: utf-8 -*-

# Imports ---------------------------------------------------------------------

import datetime
import html
import pytz
import re
from feedstream.config import settings

# Constants -------------------------------------------------------------------

RE_DIV_TAG = re.compile(r'<div\s*[^>]*?>')
RE_HEADER_TAG = re.compile(r'<h\d+\s*[^>]*?>')
RE_PARA_TAG = re.compile(r'<p\s*[^>]*?>')
RE_ARTICLE_TAG = re.compile(r'<article\s*[^>]*?>')
RE_BLOCKQUOTE_TAG = re.compile(r'<blockquote\s*[^>]*?>')
RE_FIGCAPTION_TAG = re.compile(r'<figcaption\s*[^>]*?>')
RE_LI_TAG = re.compile(r'<li\s*[^>]*?>')
RE_HR_TAG = re.compile(r'<hr\s*[^>]*?>')
RE_OTHER_TAG = re.compile(r'<[^>]+?>')
RE_WHITESPACE = re.compile(r'\s+')
RE_WHITESPACE_PUNCTUATION = re.compile(r'\s([?,;:.)}\]"](?:\s|$))')
RE_WHITESPACE_EXCLAMATION = re.compile(r'\s(!+(?:\s|$))')
RE_END_CONTINUE = re.compile(' Continue reading\.\.\.\s*$')
RE_END_DOTS = re.compile('\.\.\.\s*$')
TRUNCATE_LENGTH = 500
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
    'full_content',
    'short_content',
    'keywords',
    'comments',
    'highlights',
    'article_id']

# Timestamp functions ---------------------------------------------------------

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

# Data processing functions ---------------------------------------------------

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


def clean_text(text):

    """
    Cleans html text. Removes tags from html summaries. Tags are replaced by
    spaces and then multiple whitespace characters are replaced by a single
    space. Whitespace before puncuation is then removed, followed by any
    continue reading markers. Any leading or trailing whitespace is stripped.

    """

    # Unescape html entities
    text = html.unescape(text)

    # Replace opening block level elements with a single space
    text = re.sub(RE_DIV_TAG, ' ', text)
    text = re.sub(RE_HEADER_TAG, ' ', text)
    text = re.sub(RE_PARA_TAG, ' ', text)
    text = re.sub(RE_ARTICLE_TAG, ' ', text)
    text = re.sub(RE_BLOCKQUOTE_TAG, ' ', text)
    text = re.sub(RE_FIGCAPTION_TAG, ' ', text)
    text = re.sub(RE_LI_TAG, ' ', text)
    text = re.sub(RE_HR_TAG, ' ', text)

    # Remove all other tags completely
    text = re.sub(RE_OTHER_TAG, '', text)

    # Replace multiple whitespace characters with a single space
    text = re.sub(RE_WHITESPACE, ' ', text)

    # Remove whitespace before punctuation
    text = re.sub(RE_WHITESPACE_PUNCTUATION, r'\1', text)
    text = re.sub(RE_WHITESPACE_EXCLAMATION, r'\1', text)

    # Strip any leading or trailing whitespace and return
    return text.strip()


def truncate(text, length, marker=None):

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

# Data parsing functions ------------------------------------------------------

def parse_title(item):

    """Get the title for the item or None if missing."""

    title = get_opt_key(item, 'title')
    if title is not None:
        title = clean_text(title)
    return title

def parse_author(item):

    """Get the author for the item or None if missing."""

    author = get_opt_key(item, 'author')
    if author is not None:
        author = clean_text(author)
    return author

def parse_publisher(item):

    """Get the publisher for the item or None if missing."""

    publisher = get_opt_key(item, 'origin', 'title')
    if publisher is not None:
        publisher = clean_text(publisher)
    return publisher

def parse_url(item):

    """Get the best available url for the item or None if missing."""

    if key_exists(item, 'canonicalUrl'):
        return item['canonicalUrl']

    if key_exists(item, 'canonical'):
        for c in item['canonical']:
            if key_exists(c, 'href'):
                return c['href']

    if key_exists(item, 'alternate'):
        for a in item['alternate']:
            if key_exists(a, 'href'):
                return a['href']

    return None

def parse_pub_date(item):

    """Get the publication date or None if missing."""

    pub_date = get_opt_key(item, 'published')
    if pub_date is not None:
        pub_date = get_date_from_timestamp(pub_date)
    return pub_date

def parse_add_timestamp(item):

    """Get date and time data for the added timestamp or None if missing."""

    ats = get_opt_key(item, 'actionTimestamp')
    add_timestamp = None
    add_date = None
    add_time = None

    if ats is not None:
        add_timestamp = ats
        add_date = get_date_from_timestamp(ats)
        add_time = get_time_from_timestamp(ats).strftime('%H:%M:%S')

    return (add_timestamp, add_date, add_time)

def parse_content_fields(item):

    """
    Gets the full content and summary, and creates the short content based
    on which of these is present. The function aims to use a truncated version
    of the full content for the short content. If the full content is not
    present, it will then try to use a truncated version of the summary. If
    neither the full content nor the summary is present, all returned values
    are None.

    """

    short_content = None
    full_content = get_opt_key(item, 'fullContent')
    summary = get_opt_key(item, 'summary', 'content')

    if full_content is not None and len(clean_text(full_content)) != 0:

        full_content = clean_text(full_content)
        short_content = truncate(full_content,
            TRUNCATE_LENGTH, marker=TRUNCATE_MARKER)

        if summary is not None and len(clean_text(summary)) != 0:
            summary = clean_text(summary)
        else:
            summary = None

    else:

        full_content = None
        if summary is not None and len(clean_text(summary)) != 0:
            summary = clean_text(summary)
            short_content = truncate(summary,
                TRUNCATE_LENGTH, marker=TRUNCATE_MARKER)
        else:
            summary = None
            short_content = None

    return (short_content, full_content, summary)

def parse_keywords(item):

    """Get the keywords or None if missing."""

    keywords = get_opt_key(item, 'keywords')

    if keywords is not None:
        words = []
        for keyword in keywords:
            words.append(clean_text(keyword))

    return keywords

def parse_annotations(item):

    """
    Get comments and higlights from the annotations field or return None if
    they are missing.

    """

    annotations = get_opt_key(item, 'annotations')
    comments = None
    highlights = None

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

        if len(comments) == 0:
            comments = None

        if len(highlights) == 0:
            highlights = None

    return (comments, highlights)

def parse_item(tag_id, tag_label, item, flatten=False):

    """
    Parse an entry item returned from the API, simplify and clean the data,
    and return it as a flat dictionary.

    """

    entry = {}
    entry['tag_id'] = tag_id
    entry['tag_label'] = clean_text(tag_label)
    entry['article_id'] = item['id']
    entry['title'] = parse_title(item)
    entry['author'] = parse_author(item)
    entry['publisher'] = parse_publisher(item)
    entry['url'] = parse_url(item)
    entry['pub_date'] = parse_pub_date(item)

    # Handle added timestamp fields
    ats_fields = parse_add_timestamp(item)
    entry['add_timestamp'] = ats_fields[0]
    entry['add_date'] = ats_fields[1]
    entry['add_time'] = ats_fields[2]

    # Handle content fields
    content_fields = parse_content_fields(item)
    entry['short_content'] = content_fields[0]
    entry['full_content'] = content_fields[1]
    entry['summary'] = content_fields[2]

    # Handle keywords
    entry['keywords'] = parse_keywords(item)
    if flatten and entry['keywords'] is not None:
        entry['keywords'] = SEPARATOR.join(entry['keywords'])

    # Handle annotations
    annotations = parse_annotations(item)
    entry['comments'] = annotations[0]
    entry['highlights'] = annotations[1]

    if flatten and entry['comments'] is not None:
        entry['comments'] = SEPARATOR.join(entry['comments'])

    if flatten and entry['highlights'] is not None:
        entry['highlights'] = SEPARATOR.join(entry['highlights'])

    return entry
