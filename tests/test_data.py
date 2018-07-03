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
