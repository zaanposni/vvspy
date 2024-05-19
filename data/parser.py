import csv
from enum import Enum
import re
from collections import defaultdict

# de:08111:154:1:1
STATION_ID_REGEX = re.compile(r"de:(\d+):(\d+):(\d+):([\dA-Z]+)", re.IGNORECASE)


def sanitize_name(name):
    """Sanitize name to be a valid Python identifier"""
    return re.sub(r"\W|^(?=\d)", "_", name.upper()).strip("_")


def read_csv_with_encoding(file_path, encoding):
    stations = defaultdict(list)
    with open(file_path, encoding=encoding) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")
        for row in reader:
            name_options = set([row["Name"], row["Name mit Ort"]])
            global_id = row["Globale ID"]
            long_name = row["Steigname"] if row["Steigname"] else row["Name"]
            city = f"{row.get('Gemeinde', '')} {row.get('Teilort', '')}".strip()

            description = f"{long_name} ({city})" if city else long_name

            if not global_id:
                continue
            for name in name_options:
                if name:  # Ensure the name is not empty
                    sanitized_name = sanitize_name(name)
                    stations[sanitized_name].append((global_id, description))
    return stations


def generate_unique_enum_names(stations):
    unique_stations = {}
    for name, info in stations.items():
        if len(info) == 1:
            unique_stations[name] = (info[0][0], info[0][1])
        else:
            parsed_ids = [STATION_ID_REGEX.match(global_id).groups() for global_id, _ in info]
            all_group_1 = [parsed_id[0] for parsed_id in parsed_ids]
            all_group_2 = [parsed_id[1] for parsed_id in parsed_ids]
            if all(x == all_group_1[0] for x in all_group_1) and all(x == all_group_2[0] for x in all_group_2):
                short_id = f"de:{parsed_ids[0][0]}:{parsed_ids[0][1]}"
                unique_stations[name] = (short_id, "")

            for idx, station in enumerate(info, 1):
                unique_stations[f"{name}_{idx}"] = station
    return unique_stations


# Step 1: Read the CSV File with specified encoding
file_path = "vvs_steige.csv"
encoding = "ISO-8859-1"  # Change this to the correct encoding if necessary
stations = read_csv_with_encoding(file_path, encoding)
unique_stations = generate_unique_enum_names(stations)

# Step 2: Create the Enum
enum_content = "# This is an auto-generated file. Do not modify this file manually\n"
enum_content += "from enum import Enum\n\n"
enum_content += "class Station(Enum):\n"
enum_content += '\t"""\n'
enum_content += "\tThis enum was generated using the data/parser.py script\n"
enum_content += "\tThe data has been extracted from the VVS Steige CSV file\n"
enum_content += "\tThis enum contains all unique stations from the CSV file\n\n"
enum_content += "\tThe station names are sanitised to be valid Python identifiers\n"
enum_content += "\tThe station names are in the format: 'de:08111:154:1:1'\n"
enum_content += "\tThe last two values describe the platform and the direction and might not be included\n"
enum_content += "\tNote that even if you select a specific platform, the API will still return all possible connections\n"
enum_content += '\t"""\n\n'
for name, info in unique_stations.items():
    global_id, description = info
    if description:
        enum_content += f"\t{name} = '{global_id}'  # {description}\n"
    else:
        enum_content += f"\t{name} = '{global_id}'\n"

# Step 3: Write the Enum to stations.py
with open("../vvspy/enums/stations.py", "w", encoding="utf-8") as f:
    f.write(enum_content)

print(f"Enum created successfully in stations.py with {len(unique_stations)} stations.")
