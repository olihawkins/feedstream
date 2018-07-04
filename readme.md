# feedstream

A Python package for downloading data from the Feedly API. This is not a wrapper for the full Feedly API but a Python library that is designed to support a particular workflow, in which articles are classified in Feedly by saving them to boards and the data on the articles is downloaded for analysis.

## Usage

Simply set the API token and timezone in settings.py and download data on all articles that have been saved as entries to boards in Feedly with:

``` python
import feedstream as fs
data = fs.download_entries()
```

This function returns a dictionary with three keys:

- `downloaded` contains a Feedly timestamp of the last time data was downloaded from Feedly
- `fieldnames` is a list of the fieldnames used as keys for each entry in the `entries` list
- `entries` is a list of all entries saved to boards, along with the id and name of their board

The downloaded entries can be written to a csv in the data directory with `fs.write_entries_csv(data)`, or alternatively can be converted to a pandas dataframe with `pandas.DataFrame(data['entries'])`.

You can run the package as a program directly from the command line with `python -m feedstream`, which downloads the data to a csv in the data directory. You can set feedstream to only download articles that have been added to boards since the last time data was saved by setting `download_new` to `True` in settings.py.

## Tests
Run `python -m unittest -v` to run the unit tests.
