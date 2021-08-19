"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path="data/neos.csv"):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    # TODO: Load NEO data from the given CSV file.
    neos = []
    with open(neo_csv_path, 'r') as infile:
        reader = csv.DictReader(infile)
        for line in reader:
            neos.append(line)
    print('loaded NEO data')
    neo_collection = []
    for neo in neos:
        neo_collection.append(NearEarthObject(
            designation=neo['pdes'],
            name=neo['name'],
            diameter=neo['diameter'],
            hazardous=neo['pha']))
    print('created NearEarthObject collection')
    return neo_collection


def load_approaches(cad_json_path="data/cad.json"):
    """Read close approach data from a JSON file.

    :param neo_csv_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    # TODO: Load close approach data from the given JSON file.
    with open(cad_json_path, 'r') as infile:
        cas = json.load(infile)
    print('loaded approaches data')
    cas_collection = []
    for ca in cas['data']:
        cas_collection.append(CloseApproach(
            designation=ca[0], time=ca[3], distance=ca[4], velocity=ca[7]))
    print('created CloseApproach collection')
    return cas_collection
