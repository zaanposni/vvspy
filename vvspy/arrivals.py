from typing import List, Union
from datetime import datetime
import requests
from requests.models import Response
import json
import logging as __logging

from .enums.stations import Station
from .models import Arrival

_API_URL = "http://www3.vvs.de/vvs/widget/XML_DM_REQUEST?"
__logger = __logging.getLogger("vvspy")

def get_arrivals(
    station_id: Union[str, int, Station],
    check_time: datetime = None,
    limit: int = 100,
    request_params: dict = None,
    return_response: bool = False,
    session: requests.Session = None,
    **kwargs,
) -> Union[List[Arrival], Response, None]:
    r"""

    Returns: List[:class:`vvspy.models.Arrival`]
    Returns none on webrequest errors.

    Examples
    --------
    Basic usage:

    .. code-block:: python

        results = vvspy.get_arrivals("5006115", limit=3)  # Stuttgart main station

    Set proxy for request:

    .. code-block:: python

        proxies = {}  # see https://stackoverflow.com/a/8287752/9850709
        results = vvspy.get_arrivals("5006115", request_params={"proxies": proxies})

    Parameters
    ----------
        station_id Union[:class:`int`, :class:`str`, :class:`vvspy.enums.Station`]
            Station you want to get arrivals from.
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
            Check arrivals.py to see all available kwargs.
    """

    if not check_time:
        check_time = datetime.now()
    if request_params is None:
        request_params = dict()
    params = {
        "locationServerActive": kwargs.get(
            "locationServerActive", 1
        ),  # typo from zocationServerActive ?!
        "lsShowTrainsExplicit": kwargs.get("lsShowTrainsExplicit", 1),
        "stateless": kwargs.get("stateless", 1),
        "language": kwargs.get("language", "de"),
        "SpEncId": kwargs.get("SpEncId", 0),
        "anySigWhenPerfectNoOtherMatches": kwargs.get(
            "anySigWhenPerfectNoOtherMatches", 1
        ),
        "limit": limit,
        "depArr": "arrival",
        "type_dm": kwargs.get("type_dm", "any"),
        "anyObjFilter_dm": kwargs.get("anyObjFilter_dm", 2),
        "deleteAssignedStops": kwargs.get("deleteAssignedStops", 1),
        "name_dm": station_id.value,
        "mode": kwargs.get("mode", "direct"),
        "dmLineSelectionAll": kwargs.get("dmLineSelectionAll", 1),
        "useRealtime": kwargs.get("useRealtime", 1),  # live delay
        "outputFormat": kwargs.get("outputFormat", "json"),
        "coordOutputFormat": kwargs.get("coordOutputFormat", "WGS84[DD.ddddd]"),
        "itdDateTimeDepArr": "arr",
        "itdDateYear": check_time.strftime("%Y"),
        "itdDateMonth": check_time.strftime("%m"),
        "itdDateDay": check_time.strftime("%d"),
        "itdTimeHour": check_time.strftime("%H"),
        "itdTimeMinute": check_time.strftime("%M"),
        "itdTripDateTimeDepArr": "arr",
    }

    if session:
        r = session.get(_API_URL, **{**request_params, **{"params": params}})
    else:
        r = requests.get(_API_URL, **{**request_params, **{"params": params}})

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
        return _parse_response(r.json())
    except json.decoder.JSONDecodeError as e:
        __logger.error("Error in API request. Received invalid JSON. Status code: %s", r.status_code)
        raise e


def _parse_response(result: dict) -> List[Arrival]:
    parsed_response = []

    if (
        not result or "arrivalList" not in result or not result["arrivalList"]
    ):  # error in response/request
        return []  # no results

    if isinstance(result["arrivalList"], dict):  # one result
        parsed_response.append(Arrival(**result["arrivalList"]["arrival"]))
    elif isinstance(result["arrivalList"], list):  # multiple result
        for arrival in result["arrivalList"]:
            parsed_response.append(Arrival(**arrival))

    return parsed_response
