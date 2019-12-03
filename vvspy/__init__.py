from datetime import datetime as __datetime
from typing import List, Union

from .obj import Arrival, Departure
from .trip import get_trip
from .departures import departures


def departure_now(station_id: Union[str, int], limit: int = 100, **kwargs) -> List[Union[Arrival, Departure]]:
    return departures(station_id=station_id, check_time=__datetime.now(), limit=limit, **kwargs)

