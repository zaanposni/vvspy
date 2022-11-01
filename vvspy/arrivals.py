import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from requests import Session

from vvspy.models.arrival import Arrival
from vvspy.utils.get_request import get_request

__API_URL = "http://www3.vvs.de/vvs/widget/XML_DM_REQUEST?"


def _parse_arrivals(result: Dict[str, Any], limit: int) -> List[Arrival]:
    """Parser which selects the relevant data from the API response.
    And next converts them to Arrival objects and returns them in a list.

    Parameters
    ----------
    result : Dict[str, Any]
        The API response.
    limit : int
        Limit the number of results.

    Returns
    -------
    List[Arrival]
        A list of Arrival objects or None if a error occurred.
    """
    parsed_response = []

    try:
        parsed_response = [Arrival(**arrival) for arrival in result["arrivalList"][:limit]]
    except KeyError as err:
        logging.error("Invalid response: %s", err)
        return []
    except Exception as err:
        logging.error("Unknown error: %s", err)
        return []

    return parsed_response


def get_arrival(
    station_id: Union[str, int],
    check_time: datetime = datetime.now(),
    request_params: Optional[Dict[str, Any]] = None,
    session: Optional[Session] = None,
    **kwargs,
) -> Optional[List[Arrival]]:
    """Wrapper function for `get_arrivals()` which returns only one result.

    * TODO: Think about deleting this function.

    Parameters
    ----------
    station_id : Union[str, int]
        Station you want to get arrivals from. See csv on root of repository to get your id.
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
    Optional[List[Arrival]]
        Returns a list containing one Arrival object or None if a error occurred.
    """
    return get_arrivals(station_id, check_time, 1, request_params, session, **kwargs)


def get_arrivals(
    station_id: Union[str, int],
    check_time: datetime = datetime.now(),
    limit: int = 100,
    request_params: Optional[Dict[str, Any]] = None,
    session: Optional[Session] = None,
    **kwargs,
) -> List[Arrival]:
    """This function returns a list of arrivals for a given station id.

    * TODO: Switch from `kwargs` to dataclasses or pydantic
    * TODO: Add method to get the raw response

    Parameters
    ----------
    station_id : Union[str, int]
        Station you want to get arrivals from. See csv on root of repository to get your id.
    check_time : datetime, optional
        Time you want to check. _By default `datetime.now()`._
    limit : int, optional
        Limit requests to this integer. _By default `100`._
    request_params : Optional[Dict[str, Any]], optional
        Params parsed to the api request (e.g. proxies).
    session : Optional[Session], optional
        If set, uses a given requests.session object for requests.
    **kwargs : Dict[str, Any]
        Additional parameters to pass to the API request.

    Returns
    -------
    List[Arrival]
        Returns a list of Arrival objects.

    Examples
    --------
    The following code shows a basic example on how to use ``get_arrivals()``:

    ```python
    results = vvspy.get_arrivals("5006115", limit=3)  # Stuttgart main station
    ```

    An example for setting a proxy for the request:

    ```python
    proxies = {}  # see https://stackoverflow.com/a/8287752/9850709
    results = vvspy.get_arrivals("5006115", request_params={"proxies": proxies})
    ```
    """
    params = {
        "locationServerActive": kwargs.get("locationServerActive", 1),  # typo from zocationServerActive ?!
        "lsShowTrainsExplicit": kwargs.get("lsShowTrainsExplicit", 1),
        "stateless": kwargs.get("stateless", 1),
        "language": kwargs.get("language", "de"),
        "SpEncId": kwargs.get("SpEncId", 0),
        "anySigWhenPerfectNoOtherMatches": kwargs.get("anySigWhenPerfectNoOtherMatches", 1),
        "depArr": "arrival",
        "type_dm": kwargs.get("type_dm", "any"),
        "anyObjFilter_dm": kwargs.get("anyObjFilter_dm", 2),
        "deleteAssignedStops": kwargs.get("deleteAssignedStops", 1),
        "name_dm": station_id,
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

    if request_params is None:
        request_params = {}

    req = get_request(__API_URL, params, request_params, session)

    if req is None:
        return []

    try:
        req.encoding = "UTF-8"
        return _parse_arrivals(req.json(), limit=limit)
    except json.decoder.JSONDecodeError as err:
        logging.error("Invalid json: %s", err)
        logging.debug("Request: %s, Request text: %s", req.status_code, req.text)
        return []
