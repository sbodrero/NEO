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


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth
    objects.
    :return: A collection of `NearEarthObject`s.
    """
    neo_collection = []
    with open(neo_csv_path, 'r') as neo_csv:
        reader = csv.DictReader(neo_csv)
        for item in reader:
            neo = NearEarthObject(
                item.get('pdes', ''),
                True if item.get('pha') == 'Y' else False,
                item.get('name') if item.get('name') else None,
                float(item.get('diameter')) if item.get('diameter')
                else float('nan')
            )
            neo_collection.append(neo)
    return neo_collection


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file containing data about close
    approaches.
    :return: A collection of `CloseApproach`es.
    """
    with open(cad_json_path, 'r') as approaches:
        approaches_collection = []
        file = json.load(approaches)
        fields = file['data']
        for field in fields:
            approach = CloseApproach (
                field[0],
                field[3],
                field[4],
                field[7]
            )
            approaches_collection.append(approach)
        return approaches_collection
