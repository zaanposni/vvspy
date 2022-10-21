import json
from datetime import datetime
from typing import Any

from loguru import logger
from requests import Session

from vvspy.models.departure import Departure
from vvspy.utils.get_request import get_request

# TODO: new station id format de:08111:2599 (lapp kabel)
__API_URL = "http://www3.vvs.de/vvs/widget/XML_DM_REQUEST?"


def _parse_departures(result: dict[str, Any], limit: int) -> list[Departure]:
    """Parser which selects the relevant data from the API response.
    And next converts them to Departure objects and returns them in a list.

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
    list[Departure]
        A list of Departure objects or None if a error occurred.
    """
    parsed_response = []

    try:
        parsed_response = [Departure(**departure) for departure in result["departureList"][:limit]]
    except KeyError as err:
        logger.error(f"Invalid response: {err}")
        logger.debug(f"Response: {result}")
        return []
    except Exception as err:
        logger.error(f"Unknown error: {err}")
        logger.debug(f"Response: {result}")
        return []

    return parsed_response


def get_departures(
    station_id: str | int,
    check_time: datetime = datetime.now(),
    limit: int = 100,
    request_params: dict[str, Any] | None = None,
    session: Session | None = None,
    **kwargs: dict[str, Any],
) -> list[Departure]:
    """This function returns a list of Departure objects.

    * TODO: error handling

    Parameters
    ----------
    station_id : str | int
        Station you want to get departures from. See csv on root of repository to get your id.
    check_time : datetime, optional
        Time you want to check. By default datetime.now().
    limit : int, optional
        Limit request/result on this integer. By default 100.
    request_params : dict[str, Any] | None, optional
        Params parsed to the api request (e.g. proxies). By default None.
    session : Session | None, optional
        If set, uses a given requests.session object for requests. By default None.
    **kwargs : dict[str, Any]
        Additional parameters to pass to the API request.

    Returns
    -------
    list[Departure]
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
        logger.error("Error in API request")
        logger.debug(f"Request: {req.status_code}")
        logger.debug(f"{req.text}")
        return []
