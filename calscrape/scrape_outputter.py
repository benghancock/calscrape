"""scrape_outputter.py

Functions for outputting scrape data in different formats
"""

import csv
import sys


def output_csv(data):
    """Write scrape data as CSV to stdout"""
    header = data[0]
    writer = csv.DictWriter(
        sys.stdout,
        fieldnames=header
    )

    writer.writeheader()
    writer.writerows(data)

    return None
