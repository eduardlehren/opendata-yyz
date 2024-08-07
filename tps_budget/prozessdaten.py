import argparse
import glob
import json
import os
import requests
import shutil
import sys
import time
import yaml

from datetime import datetime
from elasticsearch import Elasticsearch


CREDS_FILE = "creds.yaml"
URL = {
    "2024": "https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/"
            "668434ee-9541-40a8-adb6-0ad805fcc9b6/resource/"
            "725e6d57-a83c-4b73-80f2-784b8014eb29/download/"
            "TPS%20Budget%202024.json",
    "2023": "https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/"
            "668434ee-9541-40a8-adb6-0ad805fcc9b6/resource/"
            "725e6d57-a83c-4b73-80f2-784b8014eb29/download/"
            "TPS%20Budget%202023.json",
    "2022": "https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/"
            "668434ee-9541-40a8-adb6-0ad805fcc9b6/resource/"
            "725e6d57-a83c-4b73-80f2-784b8014eb29/download/"
            "TPS%20Budget%202022.json",
    "2021": "https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/"
            "668434ee-9541-40a8-adb6-0ad805fcc9b6/resource/"
            "725e6d57-a83c-4b73-80f2-784b8014eb29/download/"
            "TPS%20Budget%202021.json",
    "2020": "https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/"
            "668434ee-9541-40a8-adb6-0ad805fcc9b6/resource/"
            "725e6d57-a83c-4b73-80f2-784b8014eb29/download/"
            "TPS%20Budget%202020.json"
}
YEARS_AVAILABLE = ["2020", "2021", "2022", "2023", "2024"]


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


def download_data(year_requested):
    local_filename = f"data_versions/tps-budget-{year_requested}" \
                     f"-{_generate_timestamp()}.json"
    with requests.get(URL[year_requested], stream=True) as r:
        with open(local_filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
    print("File downloaded")
    return local_filename


def output_to_console(filename):
    with open(filename, "r") as f:
        report = json.loads(f.read())

    for instance in report:
        print(json.dumps(instance, indent=2))


def populate_elasticsearch(local_filename):
    with open(CREDS_FILE, "r") as file:
        config = yaml.safe_load(file)

    es_client = Elasticsearch(
        config["elasticsearch"]["host"],
        api_key=config["elasticsearch"]["api_key"]
    )
    index = config["elasticsearch"]["index"]

    with open(local_filename, "r") as file:
        data = json.loads(file.read())

    record_count = len(data)
    print(f"Popuating {record_count} items in Elasticsearch...")
    t = time.process_time()

    for record in data:
        doc = {
            "opendata_id": record["_id"],
            "fiscal_year": record["Fiscal_Year"],
            "budget_type": record["Budget_Type"],
            "organization_entity": record["Organization_Entity"],
            "command_name": record["Command_Name"],
            "pillar_name": record["Pillar_Name"],
            "district_name": record["District_Name"],
            "unit_name": record["Unit_Name"],
            "feature_category": record["Feature_Category"],
            "cost_element": record["Cost_Element"],
            "cost_element_long_name": record["Cost_Element_Long_Name"],
            "amount": record["Amount"]
        }
        es_client.index(index=index, document=doc)

    elapsed_time = time.process_time() - t
    print(
        f"Completed ingesting {record_count} items into {index} index,"
        f" took {elapsed_time}s to complete"
    )
    return True


def run(commandopts):
    if commandopts.requested_year:
        filename = download_data(commandopts.requested_year)
    else:
        filename = _get_latest_file()

    if filename:
        if commandopts.output:
            output_to_console(filename)
            sys.exit(0)
        elif commandopts.populate:
            if populate_elasticsearch(filename):
                print("Budget report populated into Elasticsearch")
                sys.exit(0)
            else:
                print("Budget report was NOT populated into elasticsearch")
                sys.exit(1)
    else:
        print("Unable to download file, exiting.")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Prozessdaten",
        description="ETL-Tool zur Verarbeitung der TPS-Budgetdaten von "
                    "OpenData Toronto"
    )
    parser.add_argument(
        "-o",
        "--output-to-console",
        action="store_true",
        dest="output",
        help="Outputs latest data file to console, does NOT download new file"
    )
    parser.add_argument(
        "-y",
        "--year",
        action="store",
        dest="requested_year",
        help="Downloads the TPS budget for this requested year"
    )
    parser.add_argument(
        "-p",
        "--populate-elasticsearch",
        action="store_true",
        dest="populate",
        help="Populates elasticsearch with the latest data file"
    )
    commandopts = parser.parse_args()

    if commandopts.requested_year and \
       commandopts.requested_year not in YEARS_AVAILABLE:
        print(
            "You've selected a year where data is not available.\n"
            "There is data for the following years:"
        )
        for year in YEARS_AVAILABLE:
            print(f"- {year}")
        sys.exit(1)

    if commandopts.output and commandopts.populate:
        print("Error. You must use EITHER -o or -p, not both")
        sys.exit(1)

    run(commandopts)
