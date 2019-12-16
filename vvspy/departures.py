from typing import List, Union
from datetime import datetime
import requests
from requests.models import Response
import json
import traceback

from vvspy.obj import Departure

__API_URL = "http://www3.vvs.de/vvs/widget/XML_DM_REQUEST?"
# TODO: new station id format de:08111:2599 (lapp kabel)


def get_departures(station_id: Union[str, int], check_time: datetime = None, limit: int = 100, debug: bool = False,
                   request_params: dict = None, return_resp: bool = False, **kwargs)\
        -> Union[List[Departure], Response, None]:
    r"""

    Returns: List[:class:`vvspy.obj.Departure`]
    Returns none on webrequest errors.

    Examples
    --------
    Basic usage:

    .. code-block:: python

        results = vvspy.get_departures("5006115", limit=3)  # Stuttgart main station

    Set proxy for request:

    .. code-block:: python

        proxies = {}  # see https://stackoverflow.com/a/8287752/9850709
        results = vvspy.get_departures("5006115", request_params={"proxies": proxies})

    Parameters
    ----------
        station_id Union[:class:`int`, :class:`str`]
            Station you want to get departures from.
            See csv on root of repository to get your id.
        check_time Optional[:class:`datetime.datetime`]
            Time you want to check.
            default datetime.now()
        limit Optional[:class:`int`]
            Limit request/result on this integer.
            default 100
        debug Optional[:class:`bool`]
            Get advanced debug prints on failed web requests
            default False
        request_params Optional[:class:`dict`]
            params parsed to the api request (e.g. proxies)
            default {}
        return_resp Optional[:class:`bool`]
            if set, the function returns the response object of the API request.
        kwargs Optional[:class:`dict`]
            Check departures.py to see all available kwargs.

    """

    if not check_time:
        check_time = datetime.now()
    if request_params is None:
        request_params = dict()

    params = {
        "locationServerActive": kwargs.get("locationServerActive", 1),
        "lsShowTrainsExplicit": kwargs.get("lsShowTrainsExplicit", 1),
        "stateless": kwargs.get("stateless", 1),
        "language": kwargs.get("language", "de"),
        "SpEncId": kwargs.get("SpEncId", 0),
        "anySigWhenPerfectNoOtherMatches": kwargs.get("anySigWhenPerfectNoOtherMatches", 1),
        "limit": limit,
        "depArr": "departure",
        "type_dm": kwargs.get("type_dm", "any"),
        "anyObjFilter_dm": kwargs.get("anyObjFilter_dm", 2),
        "deleteAssignedStops": kwargs.get("deleteAssignedStops", 1),
        "name_dm": station_id,
        "mode": kwargs.get("mode", "direct"),
        "dmLineSelectionAll": kwargs.get("dmLineSelectionAll", 1),
        "useRealtime": kwargs.get("useRealtime", 1),  # live delay
        "outputFormat": "json",
        "coordOutputFormat": kwargs.get("coordOutputFormat", "WGS84[DD.ddddd]"),
        "itdDateYear": check_time.strftime("%Y"),
        "itdDateMonth": check_time.strftime("%m"),
        "itdDateDay": check_time.strftime("%d"),
        "itdTimeHour": check_time.strftime("%H"),
        "itdTimeMinute": check_time.strftime("%M")
    }

    try:
        r = requests.get(__API_URL, **{**request_params, **{"params": params}})
    except ConnectionError as e:
        print("ConnectionError")
        traceback.print_exc()
        return

    if r.status_code != 200:
        if debug:
            print("Error in API request")
            print(f"Request: {r.status_code}")
            print(f"{r.text}")
        return

    if return_resp:
        return r

    try:
        r.encoding = 'UTF-8'
        return _parse_response(r.json())  # TODO: error handling
    except json.decoder.JSONDecodeError:
        if debug:
            print("Error in API request")
            print("Received invalid json")
            print(f"Request: {r.status_code}")
            print(f"{r.text}")
        return


def _parse_response(result: dict) -> List[Union[Departure]]:
    parsed_response = []
    if not result or "departureList" not in result or not result["departureList"]:  # error in response/request
        return []  # no results

    if isinstance(result["departureList"], dict):  # one result
        parsed_response.append(Departure(**result["departureList"]["departure"]))
    elif isinstance(result["departureList"], list):  # multiple result
        for departure in result["departureList"]:
            parsed_response.append(Departure(**departure))

    return parsed_response
