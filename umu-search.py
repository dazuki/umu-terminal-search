#!/usr/bin/env python3
import csv
import os
import time
import requests
import argparse
import sys

CSV_URL = "https://raw.githubusercontent.com/Open-Wine-Components/umu-database/refs/heads/main/umu-database.csv"
LOCAL_CSV_FILE = "umu-database.csv"
CACHE_EXPIRY_SECONDS = 86400

def fetch_csv_data():
    if os.path.exists(LOCAL_CSV_FILE):
        file_age = time.time() - os.path.getmtime(LOCAL_CSV_FILE)
        if file_age < CACHE_EXPIRY_SECONDS:
            with open(LOCAL_CSV_FILE, "r", encoding="utf-8") as file:
                return file.read()

    response = requests.get(CSV_URL)
    response.raise_for_status()
    with open(LOCAL_CSV_FILE, "w", encoding="utf-8") as file:
        file.write(response.text)
    return response.text

def search_csv(csv_data, criteria):
    reader = csv.DictReader(csv_data.splitlines())
    matches = []

    for row in reader:
        match = True
        for field, query in criteria.items():
            if query and query.lower() not in row[field].lower():
                match = False
                break
        if match:
            matches.append(row)

    return matches

def normalize_field_name(field_name, valid_fields):
    lower_fields = {name.lower(): name for name in valid_fields}
    return lower_fields.get(field_name.lower(), None)

def display_results(results, print_field=None):
    if results:
        if print_field and len(results) == 1:
            print(results[0].get(print_field, "Field not found"))
        elif print_field and len(results) > 1:
            print(f"Found {len(results)} matches. Cannot print '{print_field}' as multiple results were found.")
            print("Displaying all results instead:\n")
            for i, row in enumerate(results, 1):
                print(f"{i}. {row['TITLE']}")
                for key, value in row.items():
                    print(f"   {key}: {value}")
                print("-" * 40)
        else:
            print(f"Found {len(results)} match(es):\n")
            for i, row in enumerate(results, 1):
                print(f"{i}. {row['TITLE']}")
                for key, value in row.items():
                    print(f"   {key}: {value}")
                print("-" * 40)
    else:
        print("No matches found.")

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Search the UMU database.",
        add_help=False,  # Disable default help
        usage="umu-search [-t TITLE] [-s STORE] [-c CODENAME] [-u UMU_ID] [--print=FIELD]"
    )
    parser.add_argument("-t", "--title", help="Search by TITLE", default=None)
    parser.add_argument("-s", "--store", help="Search by STORE", default=None)
    parser.add_argument("-c", "--codename", help="Search by CODENAME", default=None)
    parser.add_argument("-u", "--umu_id", help="Search by UMU_ID", default=None)
    parser.add_argument("--print", help="Field to print if exactly one match is found (case-insensitive, e.g., umu_id)", default=None)
    parser.add_argument("-h", "--help", action="store_true", help="Show this help message and exit")
    return parser.parse_args()

def print_help_message():
    print("""
Usage: umu-search [-t TITLE] [-s STORE] [-c CODENAME] [-u UMU_ID] [--print=FIELD]

Options:
  -t, --title    Search by TITLE (e.g., "Age of Wonders")
  -s, --store    Search by STORE (e.g., "gog")
  -c, --codename Search by CODENAME (e.g., "blobfish")
  -u, --umu_id   Search by UMU_ID (e.g., "umu-397540")
  --print        Field to print if exactly one match is found (e.g., umu_id, TITLE)
  -h, --help     Show this help message and exit

Examples:
  umu-search -t "Age of Wonders"
  umu-search -s "egs" -c "blobfish" --print="umu_id"
  umu-search -u "umu-397540" --print="title"
  """)

def main():
    try:
        args = parse_arguments()

        if args.help or not any(vars(args).values()):
            print_help_message()
            sys.exit(0)

        criteria = {
            "TITLE": args.title,
            "STORE": args.store,
            "CODENAME": args.codename,
            "UMU_ID": args.umu_id
        }

        # Fetch and search CSV data
        csv_data = fetch_csv_data()

        # Searching for matches
        results = search_csv(csv_data, criteria)

        if args.print:
            valid_fields = ["TITLE", "STORE", "CODENAME", "UMU_ID"]
            print_field = normalize_field_name(args.print, valid_fields)
            if not print_field:
                print(f"Invalid field for --print: {args.print}. Valid fields are: {', '.join(valid_fields)}")
                sys.exit(1)
        else:
            print_field = None

        display_results(results, print_field=print_field)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
