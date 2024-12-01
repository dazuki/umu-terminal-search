# umu-terminal-search

**umu-terminal-search** is a Python script for searching the UMU database by various fields and displaying results in the terminal. It supports multiple search criteria and customizable output.

### [Download as .tar.gz](https://github.com/dazuki/umu-terminal-search/raw/refs/heads/main/umu-search.tar.gz)

## Features
- Search by **TITLE**, **STORE**, **CODENAME**, or **UMU_ID**.
- Display results directly in the terminal.
- Output a specific field (e.g., `UMU_ID`) if exactly one match is found.
- Case-insensitive search and field output.
- Help message with usage examples.

## Prerequisites
- Python 3.x
- `requests` library (`pip install requests`)

## Usage
```bash
./umu-search [OPTIONS]
```

## Options

| Option                  | Description                                  |
|:------------------------|:---------------------------------------------|
| <tt>-t, --title</tt>    | Search by TITLE (e.g., "Age of Wonders")     |
| <tt>-s, --store</tt>    | Search by STORE (e.g., "gog")                |
| <tt>-c, --codename</tt> | Search by CODENAME (e.g., "blobfish")        |
| <tt>-u, --umu_id</tt>   | Search by UMU_ID (e.g., "umu-257420")        |
| <tt>--print</tt>        | Field to print if exactly one match is found (e.g., <tt>umu_id</tt>, <tt>TITLE</tt>) |
| <tt>-h, --help</tt>     | Show the help message and usage instructions |

## Examples
Search by title
```bash
./umu-search -t "Age of Wonders"
```
Search by store and codename
```bash
# Red Dead Redemption 2 (Epic Game Store)
./umu-search -s "egs" -c "heather"
```
Search by umu_id and store. Output only title if one match is found
```bash
# Ys Origin (GOG)
./umu-search -u "umu-207350" -s "gog" --print="title"
```

## UMU-Database
The script fetches and store the UMU database locally from the following URL: [UMU Database CSV](https://raw.githubusercontent.com/Open-Wine-Components/umu-database/refs/heads/main/umu-database.csv)

Fetches new version of database if the local file is older then 1 day.
