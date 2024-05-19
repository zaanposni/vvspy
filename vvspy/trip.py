from datetime import datetime, timezone
import requests
from requests.models import Response
import json
from typing import Union, List
import logging as __logging

from .enums.stations import Station
from .models import Trip

__API_URL = "https://www3.vvs.de/mngvvs/XML_TRIP_REQUEST2"
__logger = __logging.getLogger("vvspy")

def get_trips(
    origin_station_id: Union[str, int, Station],
    destination_station_id: Union[str, int, Station],
    check_time: datetime = None,
    limit: int = 100,
    request_params: dict = None,
    return_response: bool = False,
    session: requests.Session = None,
    **kwargs,
) -> Union[List[Trip], Response, None]:
    r"""

    Returns: List[:class:`vvspy.models.Trip`]
    Returns none on webrequest errors.

    Examples
    --------
    Basic usage:

    .. code-block:: python

        results = vvspy.get_trips("5006115", "5006465", limit=3)  # Stuttgart main station to Zuffenhausen

    Set proxy for request:

    .. code-block:: python

        proxies = {}  # see https://stackoverflow.com/a/8287752/9850709
        results = vvspy.get_arrivals("5006115", "5006465", request_params={"proxies": proxies})

    Parameters
    ----------
        station_id Union[:class:`int`, :class:`str`, :class:`vvspy.enums.Station`]
            Station you want to get trips from.
        check_time Optional[:class:`datetime.datetime`]
            Time you want to check.
            default datetime.now()
        limit Optional[:class:`int`]
            Limit request/result on this integer.
            default 100
        request_params Optional[:class:`dict`]
            params parsed to the api request (e.g. proxies)
            default {}
        return_response Optional[:class:`bool`]
            if set, the function returns the response object of the API request.
        session Optional[:class:`requests.Session`]
            if set, uses a given requests.session object for requests
        kwargs Optional[:class:`dict`]
            Check trips.py to see all available kwargs.
    """

    if not check_time:
        check_time = datetime.now()
    if request_params is None:
        request_params = dict()

    params = {
        "SpEncId": kwargs.get("SpEncId", "0"),
        "calcOneDirection": kwargs.get("calcOneDirection", "1"),
        "changeSpeed": kwargs.get("changeSpeed", "normal"),
        "computationType": kwargs.get("computationType", "sequence"),
        "coordOutputFormat": kwargs.get("coordOutputFormat", "EPSG:4326"),
        "cycleSpeed": kwargs.get("cycleSpeed", "14"),
        "deleteAssignedStops": kwargs.get("deleteAssignedStops", "0"),
        "deleteITPTWalk": kwargs.get("deleteITPTWalk", "0"),
        "descWithElev": kwargs.get("descWithElev", "1"),
        "illumTransfer": kwargs.get("illumTransfer", "on"),
        "imparedOptionsActive": kwargs.get("imparedOptionsActive", "1"),
        "itOptionsActive": kwargs.get("itOptionsActive", "1"),
        "itdDate": check_time.strftime("%Y%m%d"),
        "itdTime": check_time.strftime("%H%M"),
        "language": kwargs.get("language", "de"),
        "locationServerActive": kwargs.get("locationServerActive", "1"),
        "macroWebTrip": kwargs.get("macroWebTrip", "true"),
        "name_destination": destination_station_id.value,
        "name_origin": origin_station_id.value,
        "noElevationProfile": kwargs.get("noElevationProfile", "1"),
        "noElevationSummary": kwargs.get("noElevationSummary", "1"),
        "outputFormat": "rapidJSON",
        "outputOptionsActive": "1",
        "ptOptionsActive": kwargs.get("ptOptionsActive", "1"),
        "routeType": kwargs.get("routeType", "leasttime"),
        "searchLimitMinutes": kwargs.get("searchLimitMinutes", "360"),
        "securityOptionsActive": kwargs.get("securityOptionsActive", "1"),
        "serverInfo": kwargs.get("serverInfo", "1"),
        "showInterchanges": kwargs.get("showInterchanges", "1"),
        "trITArrMOT": kwargs.get("trITArrMOT", "100"),
        "trITArrMOTvalue": kwargs.get("trITArrMOTvalue", "15"),
        "trITDepMOT": kwargs.get("trITDepMOT", "100"),
        "trITDepMOTvalue": kwargs.get("trITDepMOTvalue", "15"),
        "tryToFindLocalityStops": kwargs.get("tryToFindLocalityStops", "1"),
        "type_destination": kwargs.get("type_destination", "any"),
        "type_origin": kwargs.get("type_origin", "any"),
        "useElevationData": kwargs.get("useElevationData", "1"),
        "useLocalityMainStop": kwargs.get("useLocalityMainStop", "0"),
        "useRealtime": kwargs.get("useRealtime", "1"),
        "useUT": kwargs.get("useUT", "1"),
        "version": kwargs.get("version", "10.2.10.139"),
        "w_objPrefAl": kwargs.get("w_objPrefAl", "12"),
        "w_regPrefAm": kwargs.get("w_regPrefAm", "1"),
    }

    if session:
        r = session.get(__API_URL, **{**request_params, **{"params": params}})
    else:
        r = requests.get(__API_URL, **{**request_params, **{"params": params}})

    __logger.debug(f"Request took {r.elapsed.total_seconds()}s and returned {r.status_code}")

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
        return _parse_response(r.json(), limit)
    except json.decoder.JSONDecodeError as e:
        __logger.error("Error in API request. Received invalid JSON. Status code: %s", r.status_code)
        raise e


def _parse_response(result: dict, limit: int = 100) -> Union[List[Trip], None]:
    parsed_trips = []
    if not result or "journeys" not in result or not result["journeys"]:
        return []  # no trips found
    for trip in result["journeys"][: int(limit)]:
        parsed_trips.append(Trip(**trip))

    return parsed_trips
