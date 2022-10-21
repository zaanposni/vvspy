import json
from datetime import datetime
from typing import Any

from loguru import logger
from requests import Session, get
from requests.models import Response

from vvspy.obj.arrival import Arrival

_API_URL = "http://www3.vvs.de/vvs/widget/XML_DM_REQUEST?"


def _parse_arrivals(result: dict[str, Any], limit: int) -> list[Arrival]:
    """Parser which selects the relevant data from the API response.
    And next converts them to Arrival objects and returns them in a list.

    * TODO: Abstract the parser to a separate class.
    * TODO: Add option to limit the number of results.

    Parameters
    ----------
    result : dict[str, Any]
        The API response.
    limit : int
        Limit the number of results.

    Returns
    -------
    list[Arrival]
        A list of Arrival objects or None if a error occurred.
    """
    parsed_response = []

    try:
        parsed_response = [Arrival(**arrival) for arrival in result["arrivalList"][:limit]]
    except KeyError as err:
        logger.error(f"Invalid response: {err}")
        logger.debug(f"Response: {result}")
        return []
    except Exception as err:
        logger.error(f"Unknown error: {err}")
        logger.debug(f"Response: {result}")
        return []

    return parsed_response


def get_arrivals(
    station_id: str | int,
    check_time: datetime = datetime.now(),
    limit: int = 100,
    request_params: dict[str, Any] | None = None,
    session: Session | None = None,
    return_resp: bool = False,
    **kwargs,
) -> list[Arrival] | Response | None:
    """This function returns a list of arrivals for a given station id.

    Parameters
    ----------
    station_id : str | int
        Station you want to get arrivals from. See csv on root of repository to get your id.
    check_time : datetime, optional
        Time you want to check. By default datetime.now().
    limit : int, optional
        Limit requests to this integer. By default 100.
    request_params : dict[str, Any] | None, optional
        Params parsed to the api request (e.g. proxies). By default None.
    session : Session | None, optional
        If set, uses a given requests.session object for requests. By default None#.
    return_resp : bool, optional
        If set, the function returns the response object of the API request. By default False,

    Returns
    -------
    list[Arrival] | Response | None
        Returns either a list of Arrival objects, a Response object or None.

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

    try:
        if session:
            req = session.get(_API_URL, **request_params, params=params)
        else:
            req = get(_API_URL, **request_params, params=params)

        if req.status_code != 200:
            logger.error("The API request returned a non 200 status code.")
            logger.debug(f"Request: {req.status_code}")
            logger.debug(f"Request text: {req.text}")
            return None
    except ConnectionError as err:
        logger.error(f"Connection error: {err}")
        return None

    if return_resp:
        return req

    try:
        req.encoding = "UTF-8"
        return _parse_arrivals(req.json(), limit=limit)
    except json.decoder.JSONDecodeError as err:
        logger.error(f"Invalid json: {err}")
        logger.debug(f"Request status: {req.status_code}")
        logger.debug(f"Request text: {req.text}")
        return None
