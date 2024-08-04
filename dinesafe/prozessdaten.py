import argparse
import json
import glob
import os
import requests
import shutil
import sys
import yaml

from datetime import datetime
from elasticsearch import Elasticsearch

CREDS_FILE = "creds.yaml"
ELASTICSEARCH_INDEX = "dinesafe"
URL = "https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/" \
      "b6b4f3fb-2e2c-47e7-931d-b87d22806948/resource/" \
      "e9df9d33-727e-4758-9a84-67ebefec1453/download/Dinesafe.json"


def _generate_timestamp():
    t = datetime.now()
    timestamp = t.strftime("%Y-%m-%d")
    return timestamp


def _get_latest_file():
    try:
        latest_file = max(
            glob.iglob("data_versions/*.json"),
            key=os.path.getctime
        )
    except ValueError:
        print("No file found, exiting")
        sys.exit(1)
    return latest_file


def download_data():
    local_filename = f"dinesafe-{_generate_timestamp()}.json"
    with requests.get(URL, stream=True) as r:
        with open(local_filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
    shutil.move(local_filename, f"data_versions/{local_filename}")
    print("File downloaded")
    return True


def output_to_console(filename):
    with open(filename, "r") as f:
        report = json.loads(f.read())

    for instance in report:
        print(json.dumps(instance, indent=2))


def populate_elasticsearch(index, local_filename):
    with open(CREDS_FILE, "r") as file:
        config = yaml.safe_load(file)

    es_client = Elasticsearch(
        config["elasticsearch"]["host"],
        api_key=config["elasticsearch"]["api_key"]
    )

    with open(local_filename, "r") as file:
        data = json.loads(file.read())

    for record in data:
        doc = {
            "odt_id": record["_id"],
            "establishment_id": record["Establishment ID"],
            "inspection_id": record["Inspection ID"],
            "establishment_name": record["Establishment Name"],
            "estabishment_type": record["Establishment Type"],
            "establishment_address": record["Establishment Address"],
            "establishment_status": record["Establishment Status"],
            "min_inspections_per_year": record["Min. Inspections Per Year"],
            "infraction_details": record["Infraction Details"],
            "inspection_date": record["Inspection Date"],
            "severity": record["Severity"],
            "action": record["Action"],
            "outcome": record["Outcome"],
            "amount_fined": record["Amount Fined"],
            "location_point": {
                "lat": record["Latitude"],
                "lon": record["Longitude"]
            },
            "unique_id": record["unique_id"]
        }
        resp = es_client.index(index=index, document=doc)
        print(resp["result"])

    return True


def run(commandopts):
    if commandopts.get_data:
        if download_data():
            data_filename = _get_latest_file()
    elif commandopts.latest_file:
        data_filename = _get_latest_file()

    if commandopts.output:
        output_to_console(data_filename)

    if commandopts.populate_es:
        populate_elasticsearch(ELASTICSEARCH_INDEX, data_filename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Prozessdaten",
        description="lädt die neuesten Dinesafe-Daten herunter und "
                    "verarbeitet sie"
    )
    parser.add_argument(
        "-o",
        "--output-to-console",
        action="store_true",
        dest="output",
        help="gibt Daten an die Konsole aus"
    )
    parser.add_argument(
        "-g",
        "--get-latest-data",
        action="store_true",
        dest="get_data",
        help="Downloads the latest dataset from opendata Toronto"
    )
    parser.add_argument(
        "-l",
        "--latest-data-file",
        action="store_true",
        dest="latest_file",
        help="Uses latest data file -- "
             "prevents a new file from being downloaded"
    )
    parser.add_argument(
        "-p",
        "--populate-elasticsearch",
        action="store_true",
        dest="populate_es",
        help="Populates elasticearch index with latest results"
    )
    commandopts = parser.parse_args()

    if commandopts.get_data and commandopts.latest_file:
        print("Cannot use -g and -l simultaenously. Use one or the other.")
        sys.exit(1)

    if not commandopts.get_data and not commandopts.latest_file:
        print("Must use either -g or -l, to provide a file to process")
        sys.exit(1)

    run(commandopts)
