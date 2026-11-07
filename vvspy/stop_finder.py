from requests.models import Response
from typing import Union, List
import requests
import json
import logging as __logging

from .models import Stop

__API_URL = "https://www3.vvs.de/vvsweb/XML_STOPFINDER_REQUEST"
__logger = __logging.getLogger("vvspy")


def get_stops(
    name: str,
    request_params: dict = None,
    return_response: bool = False,
    session: requests.Session = None,
    **kwargs,
) -> Union[List[Stop], Response]:
    r"""

    Returns: List[:class:`vvspy.models.Stop`]
    Both ``stop_id`` and ``global_id`` can be used as station id for all other vvspy functions.
    ``global_id`` uses the same format as :class:`vvspy.enums.Station` (e.g. ``de:08111:6118``).

    Examples
    --------
    Basic usage:

    .. code-block:: python

        results = vvspy.get_stops("Hauptbahnhof Stuttgart")
        station_id = results[0].global_id

    Set proxy for request:

    .. code-block:: python

        proxies = {}  # see https://stackoverflow.com/a/8287752/9850709
        results = vvspy.get_stops("Hauptbahnhof Stuttgart", request_params={"proxies": proxies})

    Parameters
    ----------
        name :class:`str`
            Name of the stop you are looking for.
        request_params Optional[:class:`dict`]
            params parsed to the api request (e.g. proxies)
            default {}
        return_response Optional[:class:`bool`]
            if set, the function returns the response object of the API request.
        session Optional[:class:`requests.Session`]
            if set, uses a given requests.session object for requests
        kwargs Optional[:class:`dict`]
            Check stop_finder.py to see all available kwargs.
    """

    if request_params is None:
        request_params = dict()

    params = {
        "coordListOutputFormat": kwargs.get("coordListOutputFormat", "STRING"),
        "coordOutputFormat": kwargs.get("coordOutputFormat", "WGS84[DD.ddddd]"),
        "convertPOIsITKernel2LocationServer": kwargs.get(
            "convertPOIsITKernel2LocationServer", "1"
        ),
        "excludedMeans": kwargs.get("excludedMeans", "checkbox"),
        "language": kwargs.get("language", "de"),
        "locationServerActive": kwargs.get("locationServerActive", "1"),
        "name_sf": name,
        "outputFormat": "rapidJSON",
        "serverInfo": kwargs.get("serverInfo", "1"),
        "stateless": kwargs.get("stateless", "1"),
        "suggestAppWeb": kwargs.get("suggestAppWeb", "vvs"),
        "type_sf": kwargs.get("type_sf", "any"),
        "version": kwargs.get("version", "10.6.20.22"),
    }

    if session:
        r = session.get(__API_URL, **{**request_params, **{"params": params}})
    else:
        r = requests.get(__API_URL, **{**request_params, **{"params": params}})

    __logger.debug(
        f"Request took {r.elapsed.total_seconds()}s and returned {r.status_code}"
    )

    if r.status_code != 200:
        __logger.error("Error in API request")
        __logger.error(f"Request: {r.status_code}")
        __logger.error(f"{r.text}")
        raise Exception(f"Error in API request: {r.status_code}")

    if return_response:
        return r

    __logger.debug("Initializing parsing of response...")

    try:
        r.encoding = "UTF-8"
        return _parse_response(r.json())
    except json.decoder.JSONDecodeError as e:
        __logger.error(
            "Error in API request. Received invalid JSON. Status code: %s",
            r.status_code,
        )
        raise e


def _parse_response(result: dict) -> List[Stop]:
    parsed_stops = []
    if not result or "locations" not in result:
        return []  # no stops found
    for location in result["locations"]:
        if location.get("type") == "stop":
            parsed_stops.append(Stop(**location))

    return parsed_stops
