import json
import traceback
from datetime import datetime
from typing import Any

from loguru import logger
from requests import Session, get
from requests.models import Response

from vvspy.obj.trip import Trip

__API_URL = "https://www3.vvs.de/mngvvs/XML_TRIP_REQUEST2"


def _parse_trips(result: dict[str, Any], limit: int) -> list[Trip]:
    """Parser which selects the relevant data from the API response.
    And next converts them to Departure objects and returns them in a list.

    * TODO: Abstract the parser to a separate class.
    * TODO: Add option to limit the number of results.

    Parameters
    ----------
    result : dict[str, Any]
        The API response.
    limit : int
        The maximum number of results to return.

    Returns
    -------
    list[Trip]
        A list of Departure objects or None if a error occurred.
    """
    parsed_response = []

    try:
        print(result["journeys"])
        parsed_response = [Trip(**trip) for trip in result["journeys"][:limit]]
    except KeyError as err:
        logger.error(f"Invalid response: {err}")
        logger.debug(f"Response: {result}")
        return []
    except Exception as err:
        logger.error(f"Unknown error: {err}")
        logger.debug(f"Response: {result}")
        return []

    return parsed_response


def get_trips(
    origin_station_id: str | int,
    destination_station_id: str | int,
    check_time: datetime = datetime.now(),
    request_params: dict[str, Any] | None = None,
    limit: int = 100,
    session: Session | None = None,
    return_resp: bool = False,
    **kwargs,
) -> list[Trip] | Response | None:
    """This function returns a list of Trip objects.

    * TODO: error handling

    Parameters
    ----------
    origin_station_id : str | int
        Origin station where you want to start your trip.
    destination_station_id : str | int
        Destination station where you want to end your trip.
    check_time : datetime, optional
        Time you want to check. By default datetime.now().
    request_params : dict[str, Any] | None, optional
        Params parsed to the api request (e.g. proxies). By default None.
    limit : int, optional
        Limit request/result on this integer. By default 100.
    session : Session | None, optional
        If set, uses a given requests.session object for requests. By default None.
    return_resp : bool, optional
        If set, the function returns the response object of the API request. By default False.

    Returns
    -------
    list[Trip] | Response | None
        Returns none on webrequest errors.

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

    try:
        if session:
            req = session.get(__API_URL, **{**request_params, **{"params": params}})
        else:
            req = get(__API_URL, **{**request_params, **{"params": params}})
    except ConnectionError:
        print("ConnectionError")
        traceback.print_exc()
        return None

    if req.status_code != 200:
        logger.error("Error in API request")
        logger.debug(f"Request: {req.status_code}")
        logger.debug(f"{req.text}")
        return None

    if return_resp:
        return req

    try:
        req.encoding = "UTF-8"
        return _parse_trips(req.json(), limit=limit)
    except json.decoder.JSONDecodeError:
        logger.error("Error in API request")
        logger.debug(f"Request: {req.status_code}")
        logger.debug(f"{req.text}")
        return None
