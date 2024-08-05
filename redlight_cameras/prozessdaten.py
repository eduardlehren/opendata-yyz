import argparse
import json
import requests
import shutil
import sys

from datetime import datetime


URL = "https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/" \
      "9fcff3e1-3737-43cf-b410-05acd615e27b/resource/" \
      "7e4ac806-4e7a-49d3-81e1-7a14375c9025/download/" \
      "Red%20Light%20Cameras%20Data.geojson"


def _generate_timestamp():
    t = datetime.now()
    timestamp = t.strftime("%Y-%m-%d")
    return timestamp


def download_data():
    local_filename = \
        f"data_versions/redlight_cameras-{_generate_timestamp()}.geojson"
    with requests.get(URL, stream=True) as r:
        with open(local_filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
    print("File downloaded")
    return local_filename


def clean_data(filename):
    with open(filename, "r") as f:
        data = json.loads(f.read())

    for record in data["features"]:
        del record["properties"]["_id"]

    with open(filename, "w") as f:
        json.dump(data, f)


def run():
    filename = download_data()
    if filename:
        clean_data(filename)
        print("Data cleaned")
        sys.exit(0)
    else:
        print("Unable to download file, exiting.")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Prozessdaten",
        description="bereinigt GeoJSON-Daten aus dem OpenData-Datensatz"
                    "für Rotlichtkameras"
    )
    parser.parse_args()

    run()
