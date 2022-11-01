import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from requests import Session

from vvspy.models.trip import Trip
from vvspy.utils.get_request import get_request

__API_URL = "https://www3.vvs.de/mngvvs/XML_TRIP_REQUEST2"


def _parse_trips(result: Dict[str, Any], limit: int) -> List[Trip]:
    """Parser which selects the relevant data from the API response.
    And next converts them to Departure objects and returns them in a list.

    Parameters
    ----------
    result : Dict[str, Any]
        The API response.
    limit : int
        The maximum number of results to return.

    Returns
    -------
    List[Trip]
        A list of Departure objects or None if a error occurred.
    """
    parsed_response = []

    try:
        print(result["journeys"])
        parsed_response = [Trip(**trip) for trip in result["journeys"][:limit]]
    except KeyError as err:
        logging.error("Invalid response: %s", err)
        return []
    except Exception as err:
        logging.error("Unknown error: %s", err)
        return []

    return parsed_response


def get_trip(
    origin_station_id: Union[str, int],
    destination_station_id: Union[str, int],
    check_time: datetime = datetime.now(),
    request_params: Optional[Dict[str, Any]] = None,
    session: Optional[Session] = None,
    **kwargs,
) -> List[Trip]:
    """A wrapper function for `get_trips` which returns only the first result.

    Parameters
    ----------
    origin_station_id : Union[str, int]
        Origin station where you want to start your trip.
    destination_station_id : Union[str, int]
        Destination station where you want to end your trip.
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
    List[Trip]
        Returns a list with one Trip object or a empty list if an error occurred.
    """
    return get_trips(origin_station_id, destination_station_id, check_time, 1, request_params, session, **kwargs)


def get_trips(
    origin_station_id: Union[str, int],
    destination_station_id: Union[str, int],
    check_time: datetime = datetime.now(),
    limit: int = 100,
    request_params: Optional[Dict[str, Any]] = None,
    session: Optional[Session] = None,
    **kwargs,
) -> List[Trip]:
    """This function returns a list of Trip objects.

    * TODO: error handling
    * TODO: Switch from `kwargs` to dataclasses or pydantic
    * TODO: Add method to get the raw response

    Parameters
    ----------
    origin_station_id : Union[str, int]
        Origin station where you want to start your trip.
    destination_station_id : Union[str, int]
        Destination station where you want to end your trip.
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
    List[Trip]
        Returns a list of Trip objects.

    Examples
    --------
    The following code shows a basic example on how to use ``get_trips()``:

    ```python
    results = vvspy.get_trips("5006115", "5006465", limit=3)  # Stuttgart main station to Zuffenhausen
    ```

    An example for setting a proxy for the request:

    ```python
    proxies = {}  # see https://stackoverflow.com/a/8287752/9850709
    results = vvspy.get_arrivals("5006115", "5006465", request_params={"proxies": proxies})
    ```
    """
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
        "name_destination": destination_station_id,
        "name_origin": origin_station_id,
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

    if request_params is None:
        request_params = {}

    req = get_request(__API_URL, params, request_params, session)

    if req is None:
        return []

    try:
        req.encoding = "UTF-8"
        return _parse_trips(req.json(), limit=limit)
    except json.decoder.JSONDecodeError:
        logging.error("Error in API request")
        logging.debug("Request: %s, Request text: %s", req.status_code, req.text)
        return []
