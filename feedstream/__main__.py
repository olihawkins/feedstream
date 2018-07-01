# -*- coding: utf-8 -*-

# Imports ---------------------------------------------------------------------

import feedstream.download as download

# Functions -------------------------------------------------------------------

def main():

    print("Getting data from Feedly ...")
    download.write_entries_csv(download.download_entries())

# Main ------------------------------------------------------------------------
main()
