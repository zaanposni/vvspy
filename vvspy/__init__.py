from requests.models import Response

from vvspy.obj.arrival import Arrival
from vvspy.obj.departure import Departure
from vvspy.obj.trip import Trip

# from datetime import datetime
# from typing import Any
# from requests import Session
# from vvspy.departures import get_departures
# from vvspy.arrivals import get_arrivals
# from vvspy.trips import get_trips


def departures_now(
    # station_id: str | int, session: Session | None, limit: int = 100, return_resp: bool = False, **kwargs
) -> list[Departure] | Response | None:
    """DEPRECATED: Use `get_departures` instead.

    Todo:
        * TODO: Remove this function
    """
    pass
    # return get_departures(
    #     station_id=station_id,
    #     check_time=datetime.now(),
    #     limit=limit,
    #     return_resp=return_resp,
    #     session=session,
    #     **kwargs,
    # )


def get_departure(
    # station_id: str | int,
    # check_time: datetime | None,
    # request_params: dict[Any, Any] | None,
    # session: Session | None,
    # debug: bool = False,
    # return_resp: bool = False,
    # **kwargs,
) -> list[Departure] | Response | None:
    """DEPRECATED: Use `get_departures` instead.

    Todo:
        * TODO: Remove this function
    """
    pass
    # try:
    #     departures = get_departures(
    #         station_id=station_id,
    #         check_time=check_time,
    #         limit=1,
    #         debug=debug,
    #         request_params=request_params,
    #         return_resp=return_resp,
    #         session=session,
    #         **kwargs,
    #     )

    #     if return_resp:
    #         return departures
    #     else:
    #         return departures[0]
    # except IndexError:  # no results returned
    #     if debug:
    #         print("No departures found.")
    #     return None
    # except TypeError:  # none returned | most likely an error
    #     if debug:
    #         print("Error on webrequest")
    #     return None


def get_arrival(
    # station_id: str | int,
    # check_time: datetime | None,
    # request_params: dict[Any, Any] | None,
    # session: Session | None,
    # debug: bool = False,
    # return_resp: bool = False,
    # **kwargs,
) -> list[Arrival] | Response | None:
    """DEPRECATED: Use `get_arrivals` instead.

    Todo:
        * TODO: Remove this function
    """
    pass
    # try:
    #     arrivals = get_arrivals(
    #         station_id=station_id,
    #         check_time=check_time,
    #         limit=1,
    #         debug=debug,
    #         request_params=request_params,
    #         return_resp=return_resp,
    #         session=session,
    #         **kwargs,
    #     )

    #     if return_resp:
    #         return arrivals
    #     if arrivals is not None:
    #         return arrivals[0]
    # except IndexError:  # no results returned
    #     if debug:
    #         print("No arrivals found.")
    #     return None
    # except TypeError:  # none returned | most likely an error
    #     if debug:
    #         print("Error on webrequest")
    #     return None


def get_trip(
    # origin_station_id: str | int,
    # destination_station_id: str | int,
    # check_time: datetime | None,
    # request_params: dict[Any, Any] | None,
    # session: Session | None,
    # debug: bool = False,
    # return_resp: bool = False,
    # **kwargs,
) -> list[Trip] | Response | None:
    """DEPRECATED: Use `get_trips` instead.

    Todo:
        * TODO: Remove this function
    """
    pass
    # try:
    #     trips = get_trips(
    #         origin_station_id=origin_station_id,
    #         destination_station_id=destination_station_id,
    #         check_time=check_time,
    #         limit=1,
    #         debug=debug,
    #         request_params=request_params,
    #         session=session,
    #         **kwargs,
    #     )

    #     if return_resp:
    #         return trips
    #     else:
    #         return trips[0]
    # except IndexError:  # no results returned
    #     if debug:
    #         print("No trips found.")
    #     return None
    # except TypeError:  # none returned | most likely an error
    #     if debug:
    #         print("Error on webrequest")
    #     return None
