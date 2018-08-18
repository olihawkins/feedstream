# -*- coding: utf-8 -*-

# Imports ---------------------------------------------------------------------

import datetime
import pytz
import unittest
import feedstream.data as data
from unittest.mock import patch

# Date and time data ----------------------------------------------------------

london = pytz.timezone('Europe/London')
eastern = pytz.timezone('US/Eastern')

timestamps = [1496955660000, 1430982060000, 1232470860000, 1221508860000]
isos = [
    '2017-06-08T22:01:00+01:00', '2015-05-07T08:01:00+01:00',
    '2009-01-20T17:01:00+00:00', '2008-09-15T21:01:00+01:00']
isos_eastern = [
    '2017-06-08T17:01:00-04:00', '2015-05-07T03:01:00-04:00',
    '2009-01-20T12:01:00-05:00', '2008-09-15T16:01:00-04:00']
years = [2017, 2015, 2009, 2008]
months = [6, 5, 1, 9]
days = [8, 7, 20, 15]
hours = [22, 8, 17, 21]
minutes = [1, 1, 1, 1]
seconds = [0, 0, 0, 0]

# Mocks -----------------------------------------------------------------------

def get_mock_entry():

    mock_entry = {
        'id': 'entry_id',
        'canonicalUrl': 'http://domain.com/entry',
        'canonical': [{'href': 'http://canonical.com', 'type': 'text/html'}],
        'alternate': [{'href': 'http://alternate.com', 'type': 'text/html'}],
        'title': 'Title',
        'author': 'Author',
        'origin': {'title': 'Publisher'},
        'actionTimestamp': 1530631149285,
        'published': 1530631149285,
        'summary': {'content': '<p>Some sample text</p>'},
        'fullContent': '<p>Lorem ipsum doler <b>sit</b> amet, consectetur<p>',
        'keywords': ['some', 'keywords'],
        'annotations': [
            {'comment': 'comment one'},
            {'comment': 'comment two'},
            {'highlight': {'text': 'highlight one'}},
            {'highlight': {'text': 'highlight two'}}]
        }

    return mock_entry

# Test timestamp functions ----------------------------------------------------

class TestGetDatetimeFromTimestamp(unittest.TestCase):

    """Test that get_datetime_from_timestamp returns the expected datetime."""

    def test_datetimes(self):

        for i in range(len(timestamps)):
            dt = data.get_datetime_from_timestamp(timestamps[i], london)
            self.assertEqual(dt.year, years[i])
            self.assertEqual(dt.month, months[i])
            self.assertEqual(dt.day, days[i])
            self.assertEqual(dt.hour, hours[i])
            self.assertEqual(dt.minute, minutes[i])
            self.assertEqual(dt.second, seconds[i])


class TestGetDatetimeFromTimestampEastern(unittest.TestCase):

    """
    Test that get_datetime_from_timestamp returns the expected datetime with a
    different timezone.

    """

    def test_datetimes_eastern(self):

        for i in range(len(timestamps)):
            dt = data.get_datetime_from_timestamp(timestamps[i], eastern)
            self.assertEqual(dt.year, years[i])
            self.assertEqual(dt.month, months[i])
            self.assertEqual(dt.day, days[i])
            self.assertEqual(dt.hour, hours[i] - 5)
            self.assertEqual(dt.minute, minutes[i])
            self.assertEqual(dt.second, seconds[i])


class TestGetDateFromTimestamp(unittest.TestCase):

    """Test that get_date_from_timestamp returns the expected date."""

    def test_dates(self):

        for i in range(len(timestamps)):
            d = data.get_date_from_timestamp(timestamps[i], london)
            self.assertEqual(d.year, years[i])
            self.assertEqual(d.month, months[i])
            self.assertEqual(d.day, days[i])


class TestGetTimeFromTimestamp(unittest.TestCase):

    """Test that get_time_from_timestamp returns the expected time."""

    def test_times(self):

        for i in range(len(timestamps)):
            t = data.get_time_from_timestamp(timestamps[i], london)
            self.assertEqual(t.hour, hours[i])
            self.assertEqual(t.minute, minutes[i])
            self.assertEqual(t.second, seconds[i])


class TestGetTimeFromTimestampEastern(unittest.TestCase):

    """
    Test that get_time_from_timestamp returns the expected time with a
    different timezone.

    """

    def test_times_eastern(self):

        for i in range(len(timestamps)):
            t = data.get_time_from_timestamp(timestamps[i], eastern)
            self.assertEqual(t.hour, hours[i] - 5 )
            self.assertEqual(t.minute, minutes[i])
            self.assertEqual(t.second, seconds[i])


class TestGetIsoFromTimestamp(unittest.TestCase):

    """Test that get_iso_from_timestamp returns the expected iso."""

    def test_isos(self):

        for i in range(len(timestamps)):
            iso = data.get_iso_from_timestamp(timestamps[i], london)
            self.assertEqual(iso, isos[i])


class TestGetIsoFromTimestampEastern(unittest.TestCase):

    """
    Test that get_iso_from_timestamp returns the expected iso with a
    different timezone.

    """

    def test_isos_eastern(self):

        for i in range(len(timestamps)):
            iso = data.get_iso_from_timestamp(timestamps[i], eastern)
            self.assertEqual(iso, isos_eastern[i])


class TestGetTimestampFromDatetime(unittest.TestCase):

    """
    Test that get_timestamp_from_datetime returns the expected timestamp.

    """

    def test_timestamp(self):

        for i in range(len(timestamps)):
            dt = data.get_datetime_from_timestamp(timestamps[i], london)
            ts = data.get_timestamp_from_datetime(dt)
            self.assertEqual(ts, timestamps[i])

# Test data processing functions ----------------------------------------------

class TestKeyFunctions(unittest.TestCase):

    """Test that key_exists and get_opt_key find keys in nested dicts."""

    def setUp(self):

        self.nd = {
            'a': {'aa': 1, 'ab': 2},
            'b': {'ba': 'one', 'bb': 'two', 'bc': {'bca': 'three'}},
            'c': True}

    def test_key_exists(self):

        self.assertTrue(data.key_exists(self.nd, 'a'))
        self.assertTrue(data.key_exists(self.nd, 'a', 'aa'))
        self.assertTrue(data.key_exists(self.nd, 'a', 'ab'))
        self.assertTrue(data.key_exists(self.nd, 'b'))
        self.assertTrue(data.key_exists(self.nd, 'b', 'ba'))
        self.assertTrue(data.key_exists(self.nd, 'b', 'bb'))
        self.assertTrue(data.key_exists(self.nd, 'b', 'bc'))
        self.assertTrue(data.key_exists(self.nd, 'b', 'bc', 'bca'))
        self.assertTrue(data.key_exists(self.nd, 'c'))
        self.assertFalse(data.key_exists(self.nd, 'd'))
        self.assertFalse(data.key_exists(self.nd, 'd', 'da'))

    def test_get_opt_key(self):

        self.assertEqual(data.get_opt_key(self.nd, 'a'), {'aa': 1, 'ab': 2})
        self.assertEqual(data.get_opt_key(self.nd, 'a', 'aa'), 1)
        self.assertEqual(data.get_opt_key(self.nd, 'a', 'ab'), 2)
        self.assertEqual(data.get_opt_key(self.nd, 'b', 'ba'), 'one')
        self.assertEqual(data.get_opt_key(self.nd, 'b', 'bb'), 'two')
        self.assertEqual(data.get_opt_key(self.nd, 'b', 'bc', 'bca'), 'three')
        self.assertEqual(data.get_opt_key(self.nd, 'c'), True)
        self.assertEqual(data.get_opt_key(self.nd, 'd'), None)
        self.assertEqual(data.get_opt_key(self.nd, 'd', 'da'), None)


class TestCleanText(unittest.TestCase):

    def test_unescape_entities(self):

        """
        Test that clean_text unescapes entities in summary text, and
        that unescaped whitespace characters are removed.

        """

        input = '''&#13;&#32;&#33;&#34;&#39;&amp;'''
        expected = '''!"'&'''
        self.assertEqual(data.clean_text(input), expected)

    def test_remove_tags(self):

        """Test that clean_text removes tags from summary text."""

        input = '''
        <article>
        <h1 style="font-weight: bold;">Title</h1>
        <p style="color: #ff0000;">
        An example styled paragraph with <b>bold</b> and <i>italics</i>
        </p>
        </article>
        '''

        expected = 'Title An example styled paragraph with bold and italics'
        self.assertEqual(data.clean_text(input), expected)

    def test_remove_whitespace(self):

        """
        Test that clean_text removes trailing whitespace created from tags
        removed immediately before punctuation.

        """

        input = '''
        <b>A</b>, <b>A</b>; <b>A</b>: <b>A</b>. <b>A</b>!
        <b>A</b>!! <b>A</b>? <b>A</b>) <b>A</b>] <b>A</b>}
        '''

        expected = 'A, A; A: A. A! A!! A? A) A] A}'
        self.assertEqual(data.clean_text(input), expected)


class TestTruncate(unittest.TestCase):

    def test_truncate(self):

        """
        Test that truncate cuts text to the given length, rounded to the
        nearest whole word.

        """

        input = 'An example paragraph of text.'

        self.assertEqual(data.truncate(input, length=10),
            'An')
        self.assertEqual(data.truncate(input, length=11),
            'An example')
        self.assertEqual(data.truncate(input, length=28),
            'An example paragraph of')
        self.assertEqual(data.truncate(input, length=29),
            input)

    def test_truncate_marker(self):

        """Test that truncate can apply a truncation marker."""

        input = 'An example paragraph of text.'
        m = '...'

        self.assertEqual(data.truncate(input, length=10, marker=m),
            'An ...')
        self.assertEqual(data.truncate(input, length=11, marker=m),
            'An example ...')
        self.assertEqual(data.truncate(input, length=28 ,marker=m),
            'An example paragraph of ...')
        self.assertEqual(data.truncate(input, length=29, marker=m),
            input)

    def test_truncate_empty_marker(self):

        """Test that an empty truncation marker can be set."""

        input = 'An example paragraph of text.'
        m = ''

        self.assertEqual(data.truncate(input, length=10, marker=m),
                'An ')
        self.assertEqual(data.truncate(input, length=11, marker=m),
                'An example ')
        self.assertEqual(data.truncate(input, length=28, marker=m),
            'An example paragraph of ')
        self.assertEqual(data.truncate(input, length=29, marker=m), input)

# Test data parsing functions ------------------------------------------------------

class TestParseTitle(unittest.TestCase):

    """Test that parse_title returns the expected title."""

    def test_parse_title(self):

        mock_entry = get_mock_entry()
        expected = 'Title'
        self.assertEqual(data.parse_title(mock_entry), expected)

    def test_parse_formatted_title(self):

        mock_entry = get_mock_entry()
        mock_entry['title'] = '<h1><i>Title</i></h1>'
        expected = 'Title'
        self.assertEqual(data.parse_title(mock_entry), expected)

    def test_parse_missing_title(self):

        mock_entry = get_mock_entry()
        del(mock_entry['title'])
        expected = None
        self.assertEqual(data.parse_title(mock_entry), expected)


class TestParseAuthor(unittest.TestCase):

    """Test that parse_author returns the expected author."""

    def test_parse_author(self):

        mock_entry = get_mock_entry()
        expected = 'Author'
        self.assertEqual(data.parse_author(mock_entry), expected)

    def test_parse_formatted_author(self):

        mock_entry = get_mock_entry()
        mock_entry['author'] = '<p><b>Author</b></p>'
        expected = 'Author'
        self.assertEqual(data.parse_author(mock_entry), expected)

    def test_parse_missing_author(self):

        mock_entry = get_mock_entry()
        del(mock_entry['author'])
        expected = None
        self.assertEqual(data.parse_author(mock_entry), expected)


class TestParsePublisher(unittest.TestCase):

    """Test that parse_publisher returns the expected publisher."""

    def test_parse_publisher(self):

        mock_entry = get_mock_entry()
        expected = 'Publisher'
        self.assertEqual(data.parse_publisher(mock_entry), expected)

    def test_parse_formatted_publisher(self):

        mock_entry = get_mock_entry()
        mock_entry['origin']['title'] = '<div>Publisher</div>'
        expected = 'Publisher'
        self.assertEqual(data.parse_publisher(mock_entry), expected)

    def test_parse_missing_publisher(self):

        mock_entry = get_mock_entry()
        del(mock_entry['origin'])
        expected = None
        self.assertEqual(data.parse_publisher(mock_entry), expected)


class TestParseUrl(unittest.TestCase):

    """
    Test that parse_url finds the best canonical url for an entry. This test
    incrementally removes the best candidate urls in a mock entry and checks
    that the function finds the next best candidate url after each removal.

    """

    def test_parse_url(self):

        mock_entry = get_mock_entry()

        expected = mock_entry['canonicalUrl']
        self.assertEqual(data.parse_url(mock_entry), expected)

        del mock_entry['canonicalUrl']
        expected = mock_entry['canonical'][0]['href']
        self.assertEqual(data.parse_url(mock_entry), expected)

        del mock_entry['canonical']
        expected = mock_entry['alternate'][0]['href']
        self.assertEqual(data.parse_url(mock_entry), expected)

        del mock_entry['alternate'][0]['href']
        expected = None
        self.assertEqual(data.parse_url(mock_entry), expected)


class TestParsePubDate(unittest.TestCase):

    """Test that parse_pub_date returns the expected date."""

    def test_parse_pub_date(self):

        mock_entry = get_mock_entry()
        expected = datetime.date(2018, 7, 3)
        self.assertEqual(data.parse_pub_date(mock_entry), expected)

    def test_parse_missing_pubdate(self):

        mock_entry = get_mock_entry()
        del(mock_entry['published'])
        expected = None
        self.assertEqual(data.parse_pub_date(mock_entry), expected)


class TestParseAddTimestamp(unittest.TestCase):

    """Test that parse_add_timestamp returns the expected dates and times."""

    def test_parse_add_timestamp(self):

        expected_add_timestamp = 1530631149285
        expected_add_date = datetime.date(2018, 7, 3)
        expected_add_time = '16:19:09'

        ats_fields = data.parse_add_timestamp(get_mock_entry())
        add_timestamp = ats_fields[0]
        add_date = ats_fields[1]
        add_time = ats_fields[2]

        self.assertEqual(add_timestamp, expected_add_timestamp)
        self.assertEqual(add_date, expected_add_date)
        self.assertEqual(add_time, expected_add_time)

    def test_parse_missing_add_timestamp(self):

        expected_add_timestamp = None
        expected_add_date = None
        expected_add_time = None

        mock_entry = get_mock_entry()
        del(mock_entry['actionTimestamp'])
        ats_fields = data.parse_add_timestamp(mock_entry)
        add_timestamp = ats_fields[0]
        add_date = ats_fields[1]
        add_time = ats_fields[2]

        self.assertEqual(add_timestamp, expected_add_timestamp)
        self.assertEqual(add_date, expected_add_date)
        self.assertEqual(add_time, expected_add_time)


class TestParseContentFields(unittest.TestCase):

    """Test that parse_content_fields returns the expected content fields."""

    @patch('feedstream.data.TRUNCATE_LENGTH', 15)
    def test_parse_content_fields(self):

        expected_short_content = 'Lorem ipsum {0}'.format(data.TRUNCATE_MARKER)
        expected_full_content = 'Lorem ipsum doler sit amet, consectetur'
        expected_summary = 'Some sample text'

        content_fields = data.parse_content_fields(get_mock_entry())
        short_content = content_fields[0]
        full_content = content_fields[1]
        summary = content_fields[2]

        self.assertEqual(short_content, expected_short_content)
        self.assertEqual(full_content, expected_full_content)
        self.assertEqual(summary, expected_summary)

    @patch('feedstream.data.TRUNCATE_LENGTH', 15)
    def test_parse_missing_full_content_field(self):

        expected_short_content = 'Some sample {0}'.format(data.TRUNCATE_MARKER)
        expected_full_content = None
        expected_summary = 'Some sample text'

        mock_entry = get_mock_entry()
        del(mock_entry['fullContent'])
        content_fields = data.parse_content_fields(mock_entry)
        short_content = content_fields[0]
        full_content = content_fields[1]
        summary = content_fields[2]

        self.assertEqual(short_content, expected_short_content)
        self.assertEqual(full_content, expected_full_content)
        self.assertEqual(summary, expected_summary)

    @patch('feedstream.data.TRUNCATE_LENGTH', 15)
    def test_parse_missing_content_fields(self):

        expected_short_content = None
        expected_full_content = None
        expected_summary = None

        mock_entry = get_mock_entry()
        del(mock_entry['fullContent'])
        del(mock_entry['summary'])
        content_fields = data.parse_content_fields(mock_entry)
        short_content = content_fields[0]
        full_content = content_fields[1]
        summary = content_fields[2]

        self.assertEqual(short_content, expected_short_content)
        self.assertEqual(full_content, expected_full_content)
        self.assertEqual(summary, expected_summary)


class TestParseKeywords(unittest.TestCase):

    """Test that parse_keywords returns the expected keywords."""

    def test_parse_keywords(self):

        mock_entry = get_mock_entry()
        expected_keywords = mock_entry['keywords']
        self.assertEqual(data.parse_keywords(mock_entry), expected_keywords)

    def test_parse_missing_keywords(self):

        mock_entry = get_mock_entry()
        del(mock_entry['keywords'])
        self.assertEqual(data.parse_keywords(mock_entry), None)


class TestParseAnnotations(unittest.TestCase):

    """
    Test that parse_annotations returns the expected comments and
    highlights.

    """

    def test_parse_annotations(self):

        mock_entry = get_mock_entry()
        expected_comments = ['comment one', 'comment two']
        expected_highlights = ['highlight one', 'highlight two']

        annotations = data.parse_annotations(mock_entry)
        comments = annotations[0]
        highlights = annotations[1]

        self.assertEqual(comments, expected_comments)
        self.assertEqual(highlights, expected_highlights)

    def test_parse_missing_annotations(self):

        mock_entry = get_mock_entry()
        del(mock_entry['annotations'])
        expected_comments = None
        expected_highlights = None

        annotations = data.parse_annotations(mock_entry)
        comments = annotations[0]
        highlights = annotations[1]

        self.assertEqual(comments, expected_comments)
        self.assertEqual(highlights, expected_highlights)

    def test_parse_missing_coments(self):

        mock_entry = get_mock_entry()
        del(mock_entry['annotations'][0])
        del(mock_entry['annotations'][0])

        expected_comments = None
        expected_highlights = ['highlight one', 'highlight two']

        annotations = data.parse_annotations(mock_entry)
        comments = annotations[0]
        highlights = annotations[1]

        self.assertEqual(comments, expected_comments)
        self.assertEqual(highlights, expected_highlights)

    def test_parse_missing_highlights(self):

        mock_entry = get_mock_entry()
        del(mock_entry['annotations'][3])
        del(mock_entry['annotations'][2])

        expected_comments = ['comment one', 'comment two']
        expected_highlights = None

        annotations = data.parse_annotations(mock_entry)
        comments = annotations[0]
        highlights = annotations[1]

        self.assertEqual(comments, expected_comments)
        self.assertEqual(highlights, expected_highlights)

    def test_parse_one_highlight(self):

        mock_entry = get_mock_entry()
        del(mock_entry['annotations'][3])

        expected_comments = ['comment one', 'comment two']
        expected_highlights = ['highlight one']

        annotations = data.parse_annotations(mock_entry)
        comments = annotations[0]
        highlights = annotations[1]

        self.assertEqual(comments, expected_comments)
        self.assertEqual(highlights, expected_highlights)

class TestParseItem(unittest.TestCase):

    """Test that parse_item returns the expected json."""

    @patch('feedstream.data.TRUNCATE_LENGTH', 20)
    def test_parse_item(self):

        mock_entry = get_mock_entry()
        test_entry = data.parse_item('id', 'lab', mock_entry)

        self.assertEqual(
            sorted(list(test_entry.keys())),
            sorted(data.FIELDNAMES))

        self.assertEqual(test_entry['tag_id'], 'id')
        self.assertEqual(test_entry['tag_label'], 'lab')
        self.assertEqual(test_entry['article_id'], mock_entry['id'])
        self.assertEqual(test_entry['url'], mock_entry['canonicalUrl'])
        self.assertEqual(test_entry['title'], mock_entry['title'])
        self.assertEqual(test_entry['author'], mock_entry['author'])

        self.assertEqual(test_entry['short_content'],
            'Lorem ipsum doler {0}'.format(data.TRUNCATE_MARKER))
        self.assertEqual(test_entry['full_content'],
            'Lorem ipsum doler sit amet, consectetur')
        self.assertEqual(test_entry['summary'], 'Some sample text')

        self.assertEqual(test_entry['publisher'],
            mock_entry['origin']['title'])

        self.assertEqual(test_entry['add_timestamp'],
            mock_entry['actionTimestamp'])

        self.assertEqual(test_entry['keywords'],
            mock_entry['keywords'])

        self.assertEqual(test_entry['comments'],
            ['comment one', 'comment two'])

        self.assertEqual(test_entry['highlights'],
            ['highlight one', 'highlight two'])

        self.assertEqual(test_entry['pub_date'], datetime.date(2018, 7, 3))
        self.assertEqual(test_entry['add_date'], datetime.date(2018, 7, 3))
        self.assertEqual(test_entry['add_time'], '16:19:09')

    @patch('feedstream.data.TRUNCATE_LENGTH', 20)
    def test_parse_and_flatten_item(self):

        mock_entry = get_mock_entry()
        test_entry = data.parse_item('id', 'lab', mock_entry, flatten=True)

        self.assertEqual(
            sorted(list(test_entry.keys())),
            sorted(data.FIELDNAMES))

        self.assertEqual(test_entry['tag_id'], 'id')
        self.assertEqual(test_entry['tag_label'], 'lab')
        self.assertEqual(test_entry['article_id'], mock_entry['id'])
        self.assertEqual(test_entry['url'], mock_entry['canonicalUrl'])
        self.assertEqual(test_entry['title'], mock_entry['title'])
        self.assertEqual(test_entry['author'], mock_entry['author'])

        self.assertEqual(test_entry['short_content'],
            'Lorem ipsum doler {0}'.format(data.TRUNCATE_MARKER))
        self.assertEqual(test_entry['full_content'],
            'Lorem ipsum doler sit amet, consectetur')
        self.assertEqual(test_entry['summary'], 'Some sample text')

        self.assertEqual(test_entry['publisher'],
            mock_entry['origin']['title'])

        self.assertEqual(test_entry['add_timestamp'],
            mock_entry['actionTimestamp'])

        self.assertEqual(test_entry['keywords'],
            data.SEPARATOR.join(mock_entry['keywords']))

        self.assertEqual(test_entry['comments'],
            data.SEPARATOR.join(['comment one', 'comment two']))

        self.assertEqual(test_entry['highlights'],
            data.SEPARATOR.join(['highlight one', 'highlight two']))

        self.assertEqual(test_entry['pub_date'], datetime.date(2018, 7, 3))
        self.assertEqual(test_entry['add_date'], datetime.date(2018, 7, 3))
        self.assertEqual(test_entry['add_time'], '16:19:09')
