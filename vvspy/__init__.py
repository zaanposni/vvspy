from datetime import datetime as __datetime
from typing import List as __List
from typing import Union as __Union

from .obj import Arrival as __Arrival
from .obj import Departure as __Departure
from .obj import Trip as __Trip
from .trip import get_trips
from .departures import get_departures
from .arrivals import get_arrivals


def departures_now(station_id: __Union[str, int], limit: int = 100,
                   **kwargs) -> __List[__Union[__Arrival, __Departure]]:
    """
        Same as `get_departures`
        But `datetime.datetime.now()` is already used as parameter.

        Returns: List[:class:`vvspy.obj.Departure`]
        Returns none on webrequest errors or no results found.

    """
    return get_departures(station_id=station_id, check_time=__datetime.now(), limit=limit, **kwargs)


def get_departure(station_id: __Union[str, int], check_time: __datetime = None, debug: bool = False,
                  request_params: dict = None, **kwargs) -> __Union[__Departure, None]:
    """
    Same as `get_departures`
    But limited to one obj as result.

    Returns: :class:`vvspy.obj.Departure`
    Returns none on webrequest errors or no results found.

    """
    try:
        return get_departures(station_id=station_id, check_time=check_time, limit=1, debug=debug,
                              request_params=request_params, **kwargs)[0]
    except IndexError:  # no results returned
        if debug:
            print("No departures found.")
        return
    except TypeError:  # none returned | most likely an error
        if debug:
            print("Error on webrequest")
        return


def get_arrival(station_id: __Union[str, int], check_time: __datetime = None, debug: bool = False,
                request_params: dict = None, **kwargs) -> __Union[__Arrival, None]:
    """
        Same as `get_arrivals`
        But limited to one obj as result.

        Returns: :class:`vvspy.obj.Arrival`
        Returns none on webrequest errors or no results found.

    """
    try:
        return get_arrivals(station_id=station_id, check_time=check_time, limit=1, debug=debug,
                            request_params=request_params, **kwargs)[0]
    except IndexError:  # no results returned
        if debug:
            print("No arrivals found.")
        return
    except TypeError:  # none returned | most likely an error
        if debug:
            print("Error on webrequest")
        return


def get_trip(origin_station_id: __Union[str, int], destination_station_id: __Union[str, int],
             check_time: __datetime = None, debug: bool = False,
             request_params: dict = None, **kwargs) -> __Union[__Trip, None]:
    """
        Same as `get_trips`
        But limited to one obj as result.

        Returns: :class:`vvspy.obj.Trip`
        Returns none on webrequest errors or no results found.

    """
    try:
        return get_trips(origin_station_id=origin_station_id, destination_station_id=destination_station_id,
                         check_time=check_time, limit=1, debug=debug, request_params=request_params, **kwargs)[0]
    except IndexError:  # no results returned
        if debug:
            print("No trips found.")
        return
    except TypeError:  # none returned | most likely an error
        if debug:
            print("Error on webrequest")
        return
