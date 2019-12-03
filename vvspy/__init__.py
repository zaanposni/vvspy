from datetime import datetime as __datetime
from typing import List as __List
from typing import Union as __Union

from .obj import Arrival as __Arrival
from .obj import Departure as __Departure
from .trip import get_trip
from .departures import get_departures


def departure_now(station_id: __Union[str, int], limit: int = 100, **kwargs) -> __List[__Union[__Arrival, __Departure]]:
    return get_departures(station_id=station_id, check_time=__datetime.now(), limit=limit, **kwargs)

