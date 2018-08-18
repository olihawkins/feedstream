# feedstream

A Python package for downloading data from the Feedly API. This is not a wrapper for the full Feedly API but a Python library that is designed to support a particular workflow, in which articles are classified in Feedly by saving them to boards and the data on the articles is downloaded for analysis.

## Usage

Simply set the API token and timezone in config.json and download data on all articles that have been saved as entries to boards in Feedly with:

``` python
import feedstream as fs
download = fs.download_entries()
```

This returns a dictionary with three keys:

- `timestamp` contains a Feedly timestamp of the time this data was downloaded from Feedly
- `fieldnames` is a list of the fieldnames used as keys for each item in the `items` list
- `entries` is a list of all entries saved to boards, along with the id and name of their board

Entries can be downloaded directly to a csv with `fs.download_entries_csv()`, or to a pandas dataframe with `timestamp, df = fs.download_entries_df()`.

You can run the package as a program directly from the command line with `python -m feedstream`, which downloads the data to a csv in the application data directory. You can set feedstream to only download articles that have been added to boards since the last time data was saved by setting `download_new` to `True` in config.json.

## Tests
Run `python -m unittest -v` to run the unit tests.
