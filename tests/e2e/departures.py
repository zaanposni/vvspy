from datetime import datetime
import unittest
import sys

sys.path.append("..")

from vvspy import get_departure, get_departures
from vvspy.models import Departure
from vvspy.enums import Station


class DepartureE2E(unittest.TestCase):
    def get_next_monday_noon(self) -> datetime:
        now = datetime.now()
        while now.weekday() != 0:
            now = now.replace(day=now.day + 1)
        return now.replace(hour=12, minute=0, second=0, microsecond=0)

    def departures_enum(self):
        departures = get_departures(
            station_id=Station.HAUPTBAHNHOF__TIEF,
            check_time=self.get_next_monday_noon(),
            limit=5,
        )
        self.assertIsNotNone(departures)
        self.assertIsInstance(departures, list)
        self.assertNotEqual(len(departures), 0)
        for departure in departures:
            self.assertIsInstance(departure, Departure)

    def departure_enum(self):
        departure = get_departure(
            station_id=Station.HAUPTBAHNHOF__TIEF,
            check_time=self.get_next_monday_noon(),
        )
        self.assertIsNotNone(departure)
        self.assertIsInstance(departure, Departure)

    def departures_id(self):
        departures = get_departures(
            station_id="de:08111:6118",
            check_time=self.get_next_monday_noon(),
            limit=5,
        )
        self.assertIsNotNone(departures)
        self.assertIsInstance(departures, list)
        self.assertNotEqual(len(departures), 0)
        for departure in departures:
            self.assertIsInstance(departure, Departure)

    def departure_id(self):
        departure = get_departure(
            station_id="de:08111:6118",
            check_time=self.get_next_monday_noon(),
        )
        self.assertIsNotNone(departure)
        self.assertIsInstance(departure, Departure)

    def test_start(self):
        print("e2e departures enum")
        self.departures_enum()
        print("e2e departure enum")
        self.departure_enum()
        print("e2e departures id")
        self.departures_id()
        print("e2e departure id")
        self.departure_id()
