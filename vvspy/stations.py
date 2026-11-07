import requests

# This is a simple script that I made so you
# can look your station and its id up.

# Running get_stops will return a list of possible
# matches for the station youre looking for.

COMMON_PARAMS = {
    "excludedMeans": "checkbox",
    "coordListOutputFormat": "STRING",
    "coordOutputFormat": "WGS84[DD.ddddd]",
    "locationServerActive": "1",
    "stateless": "1",
    "serverInfo": "1",
    "outputFormat": "rapidJSON",
    "version": "10.6.20.22",
    "suggestAppWeb": "vvs",
    "convertPOIsITKernel2LocationServer": "1",
    "type_sf": "any",
    "language": "de",
}
BASE_URL = "https://www3.vvs.de/vvsweb/XML_STOPFINDER_REQUEST"

# I scraped the COMMON_PARAMS from a server request made by the VVS website.


def get_stops(inputStr: str):
    try:
        params = {**COMMON_PARAMS, "name_sf": inputStr}
        r = requests.get(BASE_URL, params=params, timeout=10)
        r.raise_for_status()
        response = r.json()
        out = []
        for loc in response.get("locations", []):
            if loc.get("type") == "stop":
                item = {
                    "name": loc.get("name"),
                    "coord": loc.get("coord"),
                    "parent": loc.get("parent", {}).get("name"),
                    "matchQuality": loc.get("matchQuality"),
                    "stopId": loc.get("properties", {}).get("stopId"),
                }

                out.append(item)
        return out

    except requests.RequestException as e:
        raise e
