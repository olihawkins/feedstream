# -*- coding: utf-8 -*-

# Imports ---------------------------------------------------------------------

import datetime
import pytz
import unittest
import feedstream.data as data

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
        'summary': {'content': '<p>Lorem ipsum.</p> <p>Doler <b>sit</b> amet'},
        'keywords': ['some', 'keywords'],
        'annotations': [
            {'comment': 'comment one'},
            {'comment': 'comment two'},
            {'highlight': {'text': 'highlight one'}},
            {'highlight': {'text': 'highlight two'}}]
        }

    return mock_entry

# Tests -----------------------------------------------------------------------

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
        <h1>Title</h1>
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

    def test_remove_markers(self):

        """Test that clean_text removes continue reading markers."""

        input = 'An example paragraph of text. Continue reading...'
        expected = 'An example paragraph of text.'
        self.assertEqual(data.clean_text(input), expected)

        input = 'An example paragraph of text. ...'
        expected = 'An example paragraph of text.'
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


class TestGetEntryUrl(unittest.TestCase):

    """
    Test that get_entry_url finds the best canonical url for an entry. This
    test incrementally removes the best candidate urls in a mock entry and
    checks that the function finds the next best candidate url after each
    removal.

    """

    def test_get_entry_url(self):

        mock_entry = get_mock_entry()

        expected = mock_entry['canonicalUrl']
        self.assertEqual(data.get_entry_url(mock_entry), expected)

        del mock_entry['canonicalUrl']
        expected = mock_entry['canonical'][0]['href']
        self.assertEqual(data.get_entry_url(mock_entry), expected)

        del mock_entry['canonical']
        expected = mock_entry['alternate'][0]['href']
        self.assertEqual(data.get_entry_url(mock_entry), expected)

        del mock_entry['alternate'][0]['href']
        expected = None
        self.assertEqual(data.get_entry_url(mock_entry), expected)


class TestParseEntry(unittest.TestCase):

    """Test that parse_entry returns the expected json."""

    def test_parse_entry(self):

        mock_entry = get_mock_entry()
        test_entry = data.parse_entry('id', 'lab', mock_entry)

        self.assertEqual(
            sorted(list(test_entry.keys())),
            sorted(data.FIELDNAMES))
        self.assertEqual(test_entry['tag_id'], 'id')
        self.assertEqual(test_entry['tag_label'], 'lab')
        self.assertEqual(test_entry['article_id'], mock_entry['id'])
        self.assertEqual(test_entry['url'], mock_entry['canonicalUrl'])
        self.assertEqual(test_entry['title'], mock_entry['title'])
        self.assertEqual(test_entry['author'], mock_entry['author'])
        self.assertEqual(test_entry['summary'], 'Lorem ipsum. Doler sit amet')

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
