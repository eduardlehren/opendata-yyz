import argparse
import json
import requests
import shutil

from datetime import datetime

URL = "https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/" \
      "b6b4f3fb-2e2c-47e7-931d-b87d22806948/resource/" \
      "e9df9d33-727e-4758-9a84-67ebefec1453/download/Dinesafe.json"


def _generate_timestamp():
    t = datetime.now()
    timestamp = t.strftime("%Y-%m-%d")
    return timestamp


def download_data():
    local_filename = f"dinesafe-{_generate_timestamp()}.json"
    with requests.get(URL, stream=True) as r:
        with open(local_filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
    print("File downloaded")
    return local_filename


def output_to_console(filename):
    with open(filename, "r") as f:
        report = json.loads(f.read())

    for instance in report:
        print(json.dumps(instance, indent=2))


def run(commandopts):
    # download_data()

    if commandopts.output:
        output_to_console("dinesafe-2024-07-21.json")


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
    # parser.add_argument(
    #     "-i",
    #     "--input-file",
    #     action="store",
    #     dest="input_file",
    #     help="Input filename",
    #     required=True
    # )
    # parser.add_argument(
    #     "-t",
    #     "--transcribe-only",
    #     action="store_true",
    #     dest="transcribe_only",
    #     help="Skips summary generation and only provides a transcription"
    # )
    # parser.add_argument(
    #     "-ot",
    #     "--transcription-output",
    #     action="store",
    #     dest="transcription_output",
    #     help="Output filename for transcription"
    # )
    # parser.add_argument(
    #     "-os",
    #     "--summary-output",
    #     action="store",
    #     dest="summary_output",
    #     help="Output filename for summary"
    # )

    commandopts = parser.parse_args()
    run(commandopts)
