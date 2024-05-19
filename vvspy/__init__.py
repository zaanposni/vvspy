from datetime import datetime as __datetime
from typing import List as __List
from typing import Union as __Union
from requests.models import Response as __Response
from requests import Session
import logging as __logging

from .enums import Station
from .models import Arrival as __Arrival
from .models import Departure as __Departure
from .models import Trip as __Trip
from .trip import get_trips
from .departures import get_departures
from .arrivals import get_arrivals


__logger = __logging.getLogger("vvspy")

def departures_now(
    station_id: __Union[str, int, Station],
    limit: int = 100,
    return_resp: bool = False,
    session: Session = None,
    **kwargs,
) -> __Union[__List[__Departure], __Response, None]:
    """
    Same as `get_departures`
    But `datetime.datetime.now()` is already used as parameter.

    Returns: List[:class:`vvspy.models.Departure`]
    Returns none on webrequest errors or no results found.

    """
    return get_departures(
        station_id=station_id,
        check_time=__datetime.now(),
        limit=limit,
        return_resp=return_resp,
        session=session,
        **kwargs,
    )


def get_departure(
    station_id: __Union[str, int, Station],
    check_time: __datetime = None,
    debug: bool = False,
    request_params: dict = None,
    return_resp: bool = False,
    session: Session = None,
    **kwargs,
) -> __Union[__Departure, __Response, None]:
    """
    Same as `get_departures`
    But limited to one obj as result.

    Returns: :class:`vvspy.models.Departure`
    Returns none on webrequest errors or no results found.

    """
    try:
        if return_resp:
            return get_departures(
                station_id=station_id,
                check_time=check_time,
                limit=1,
                debug=debug,
                request_params=request_params,
                return_resp=return_resp,
                session=session,
                **kwargs,
            )
        else:
            return get_departures(
                station_id=station_id,
                check_time=check_time,
                limit=1,
                debug=debug,
                request_params=request_params,
                return_resp=return_resp,
                session=session,
                **kwargs,
            )[0]
    except IndexError as e:  # no results returned
        __logger.error(f"No departures found. {e}")
        raise e
    except TypeError as e:  # none returned | most likely an error
        __logger.error(f"Error on webrequest. {e}")
        raise e


def get_arrival(
    station_id: __Union[str, int, Station],
    check_time: __datetime = None,
    debug: bool = False,
    request_params: dict = None,
    return_resp: bool = False,
    session: Session = None,
    **kwargs,
) -> __Union[__Arrival, __Response, None]:
    """
    Same as `get_arrivals`
    But limited to one obj as result.

    Returns: :class:`vvspy.models.Arrival`
    Returns none on webrequest errors or no results found.

    """
    try:
        if return_resp:
            return get_arrivals(
                station_id=station_id,
                check_time=check_time,
                limit=1,
                debug=debug,
                request_params=request_params,
                return_resp=return_resp,
                session=session,
                **kwargs,
            )
        else:
            return get_arrivals(
                station_id=station_id,
                check_time=check_time,
                limit=1,
                debug=debug,
                request_params=request_params,
                return_resp=return_resp,
                session=session,
                **kwargs,
            )[0]
    except IndexError as e:  # no results returned
        __logger.error(f"No arrivals found. {e}")
        raise e
    except TypeError as e:  # none returned | most likely an error
        __logger.error(f"Error on webrequest. {e}")
        raise e


def get_trip(
    origin_station_id: __Union[str, int, Station],
    destination_station_id: __Union[str, int, Station],
    check_time: __datetime = None,
    debug: bool = False,
    request_params: dict = None,
    return_resp: bool = False,
    session: Session = None,
    **kwargs,
) -> __Union[__Trip, __Response, None]:
    """
    Same as `get_trips`
    But limited to one obj as result.

    Returns: :class:`vvspy.models.Trip`
    Returns none on webrequest errors or no results found.

    """
    try:
        if return_resp:
            return get_trips(
                origin_station_id=origin_station_id,
                destination_station_id=destination_station_id,
                check_time=check_time,
                limit=1,
                debug=debug,
                request_params=request_params,
                return_resp=return_resp,
                session=session,
                **kwargs,
            )
        else:
            return get_trips(
                origin_station_id=origin_station_id,
                destination_station_id=destination_station_id,
                check_time=check_time,
                limit=1,
                debug=debug,
                request_params=request_params,
                session=session,
                **kwargs,
            )[0]
    except IndexError as e:
        __logger.error(f"No trips found. {e}")
        raise e
    except TypeError as e:
        __logger.error(f"Error on webrequest. {e}")
        raise e
