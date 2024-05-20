from datetime import datetime
import unittest
import sys

sys.path.append("..")

from vvspy import get_arrival, get_arrivals
from vvspy.models import Arrival
from vvspy.enums import Station


class ArrivalE2E(unittest.TestCase):
    def get_next_monday_noon(self) -> datetime:
        now = datetime.now()
        while now.weekday() != 0:
            now = now.replace(day=now.day + 1)
        return now.replace(hour=12, minute=0, second=0, microsecond=0)

    def arrivals_enum(self):
        arrivals = get_arrivals(
            station_id=Station.HAUPTBAHNHOF__TIEF,
            datetime=self.get_next_monday_noon(),
            limit=5,
        )
        self.assertIsNotNone(arrivals)
        self.assertIsInstance(arrivals, list)
        self.assertNotEqual(len(arrivals), 0)
        for arrival in arrivals:
            self.assertIsInstance(arrival, Arrival)

    def arrival_enum(self):
        arrival = get_arrival(
            station_id=Station.HAUPTBAHNHOF__TIEF,
            datetime=self.get_next_monday_noon(),
        )
        self.assertIsNotNone(arrival)
        self.assertIsInstance(arrival, Arrival)

    def arrivals_id(self):
        arrivals = get_arrivals(
            station_id="de:08111:6118",
            datetime=self.get_next_monday_noon(),
            limit=5,
        )
        self.assertIsNotNone(arrivals)
        self.assertIsInstance(arrivals, list)
        self.assertNotEqual(len(arrivals), 0)
        for arrival in arrivals:
            self.assertIsInstance(arrival, Arrival)

    def arrival_id(self):
        arrival = get_arrival(
            station_id="de:08111:6118",
            datetime=self.get_next_monday_noon(),
        )
        self.assertIsNotNone(arrival)
        self.assertIsInstance(arrival, Arrival)

    def test_start(self):
        print("e2e arrivals enum")
        self.arrivals_enum()
        print("e2e arrival enum")
        self.arrival_enum()
        print("e2e arrivals id")
        self.arrivals_id()
        print("e2e arrival id")
        self.arrival_id()
