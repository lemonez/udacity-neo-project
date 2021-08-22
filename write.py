"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.

You'll edit this file in Part 4.
"""
import csv
import json

import helpers


def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`. Roughly, each output row
    corresponds to the information in a single close approach from the `results`
    stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    fieldnames = ('datetime_utc', 'distance_au', 'velocity_km_s', 'designation',
                  'name', 'diameter_km', 'potentially_hazardous')
    with open(filename, 'w') as outfile:
        ca_writer = csv.writer(outfile)
        ca_writer.writerow(fieldnames)
        if not results:
            return None
        for item in results:
            name = item.neo.name
            if name is None:
                name = ""
            to_write = (
                item.time,
                item.distance,
                item.velocity,
                item.neo.designation,
                name,
                item.neo.diameter,
                str(item.neo.hazardous)
            )
            ca_writer.writerow(to_write)


def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`. Roughly, the output is a
    list containing dictionaries, each mapping `CloseApproach` attributes to
    their values and the 'neo' key mapping to a dictionary of the associated
    NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    to_write = []
    for item in results:
        to_write.append(format_ca(item))
    with open(filename, 'w') as outfile:
        json.dump(to_write, outfile)


def format_ca(ca):
    """Format CloseApproach object for JSON output."""
    name = ca.neo.name
    if name is None:
        name = ""
    km = ca.neo.diameter
    if km is None:
        km = float('nan')
    item = {}
    item['datetime_utc'] = helpers.datetime_to_str(ca.time)
    item['distance_au'] = float(ca.distance)
    item['velocity_km_s'] = float(ca.velocity)
    item['neo'] = {}
    item['neo']['designation'] = ca.neo.designation
    item['neo']['name'] = name
    item['neo']['diameter_km'] = km
    item['neo']['potentially_hazardous'] = ca.neo.hazardous
    return item
