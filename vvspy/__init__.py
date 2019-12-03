from datetime import datetime as __datetime

from .trip import get_trip
from .departures import departures


def departure_now(station_id: str, limit: int = 100, request_params: dict = None, **kwargs):
    departures(station_id=station_id, check_time=__datetime.now(), limit=limit, config=kwargs,
               request_params=request_params)
