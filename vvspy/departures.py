import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from requests import Session

from vvspy.models.departure import Departure
from vvspy.utils.get_request import get_request

__API_URL = "http://www3.vvs.de/vvs/widget/XML_DM_REQUEST?"


def _parse_departures(result: Dict[str, Any], limit: int) -> List[Departure]:
    """Parser which selects the relevant data from the API response.
    And next converts them to Departure objects and returns them in a list.

    Parameters
    ----------
    result : Dict[str, Any]
        The API response.
    limit : int
        Limit the number of results.

    Returns
    -------
    List[Departure]
        A list of Departure objects or None if a error occurred.
    """
    parsed_response = []

    try:
        parsed_response = [Departure(**departure) for departure in result["departureList"][:limit]]
    except KeyError as err:
        logging.error("Invalid response: %s", err)
        return []
    except Exception as err:
        logging.error("Unknown error: %s", err)
        return []

    return parsed_response


def get_departure(
    station_id: Union[str, int],
    check_time: datetime = datetime.now(),
    request_params: Optional[Dict[str, Any]] = None,
    session: Optional[Session] = None,
    **kwargs,
) -> List[Departure]:
    """This function is a wrapper for `get_departures()` which returns only one result.

    * TODO: Think about deleting this function.

    Parameters
    ----------
    station_id : Union[str, int]
        Station you want to get departures from. See csv on root of repository to get your id.
    check_time : datetime, optional
        Time you want to check. _By default `datetime.now()`._
    request_params : Optional[Dict[str, Any]], optional
        Params parsed to the api request (e.g. proxies).
    session : Optional[Session], optional
        If set, uses a given requests.session object for requests.
    **kwargs : Dict[str, Any]
        Additional parameters to pass to the API request.

    Returns
    -------
    List[Departure]
        A list containing one Departure object or None if a error occurred.
    """
    return get_departures(station_id, check_time, 1, request_params, session, **kwargs)


def get_departures(
    station_id: Union[str, int],
    check_time: datetime = datetime.now(),
    limit: int = 100,
    request_params: Optional[Dict[str, Any]] = None,
    session: Optional[Session] = None,
    **kwargs,
) -> List[Departure]:
    """This function returns a list of Departure objects.

    * TODO: error handling
    * TODO: Switch from `kwargs` to dataclasses or pydantic
    * TODO: new station id format de:08111:2599 (lapp kabel)
    * TODO: Add method to get the raw response

    Parameters
    ----------
    station_id : Union[str, int]
        Station you want to get departures from. See csv on root of repository to get your id.
    check_time : datetime, optional
        Time you want to check. _By default `datetime.now()`._
    limit : int, optional
        Limit request/result on this integer. _By default `100`._
    request_params : Optional[Dict[str, Any]], optional
        Params parsed to the api request (e.g. proxies).
    session : Optional[Session], optional
        If set, uses a given requests.session object for requests.
    **kwargs : Dict[str, Any]
        Additional parameters to pass to the API request.

    Returns
    -------
    List[Departure]
        Returns a list of Departure objects.

    Examples
    --------
    The following code shows a basic example on how to use ``get_departures()``::

    ```python
    results = vvspy.get_departures("5006115", limit=3)  # Stuttgart main station
    ```

    An example for setting a proxy for the request::

    ```python
    proxies = {}  # see https://stackoverflow.com/a/8287752/9850709
    results = vvspy.get_departures("5006115", request_params={"proxies": proxies})
    ```
    """
    params = {
        "locationServerActive": kwargs.get("locationServerActive", 1),
        "lsShowTrainsExplicit": kwargs.get("lsShowTrainsExplicit", 1),
        "stateless": kwargs.get("stateless", 1),
        "language": kwargs.get("language", "de"),
        "SpEncId": kwargs.get("SpEncId", 0),
        "anySigWhenPerfectNoOtherMatches": kwargs.get("anySigWhenPerfectNoOtherMatches", 1),
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
        "itdTimeMinute": check_time.strftime("%M"),
    }

    if request_params is None:
        request_params = {}

    req = get_request(__API_URL, params, request_params, session)

    if req is None:
        return []

    try:
        req.encoding = "UTF-8"
        return _parse_departures(req.json(), limit=limit)
    except json.decoder.JSONDecodeError:
        logging.error("Error in API request")
        logging.debug("Request: %s, Request text: %s", req.status_code, req.text)
        return []
