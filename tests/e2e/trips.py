from datetime import datetime
import unittest
import sys

sys.path.append("..")

from vvspy import get_trips, get_trip
from vvspy.models import Trip
from vvspy.enums import Station


class TripE2E(unittest.TestCase):
    def get_next_monday_noon(self) -> datetime:
        now = datetime.now()
        while now.weekday() != 0:
            now = now.replace(day=now.day + 1)
        return now.replace(hour=12, minute=0, second=0, microsecond=0)

    def trips_enum_enum(self):
        trips = get_trips(
            origin_station_id=Station.VAIHINGEN,
            destination_station_id=Station.HAUPTBAHNHOF__TIEF,
            check_time=self.get_next_monday_noon(),
            limit=5,
        )
        self.assertIsNotNone(trips)
        self.assertIsInstance(trips, list)
        self.assertNotEqual(len(trips), 0)
        for trip in trips:
            self.assertIsInstance(trip, Trip)

    def trip_enum_enum(self):
        trip = get_trip(
            origin_station_id=Station.VAIHINGEN,
            destination_station_id=Station.HAUPTBAHNHOF__TIEF,
            check_time=self.get_next_monday_noon(),
        )
        self.assertIsNotNone(trip)
        self.assertIsInstance(trip, Trip)

    def trips_enum_id(self):
        trips = get_trips(
            origin_station_id=Station.VAIHINGEN,
            destination_station_id="de:08111:6118",
            check_time=self.get_next_monday_noon(),
            limit=5,
        )
        self.assertIsNotNone(trips)
        self.assertIsInstance(trips, list)
        self.assertNotEqual(len(trips), 0)
        for trip in trips:
            self.assertIsInstance(trip, Trip)

    def trip_enum_id(self):
        trip = get_trip(
            origin_station_id=Station.VAIHINGEN,
            destination_station_id="de:08111:6118",
            check_time=self.get_next_monday_noon(),
        )
        self.assertIsNotNone(trip)
        self.assertIsInstance(trip, Trip)

    def trips_id_id(self):
        trips = get_trips(
            origin_station_id="de:08111:6002",
            destination_station_id="de:08111:6118",
            check_time=self.get_next_monday_noon(),
            limit=5,
        )
        self.assertIsNotNone(trips)
        self.assertIsInstance(trips, list)
        self.assertNotEqual(len(trips), 0)
        for trip in trips:
            self.assertIsInstance(trip, Trip)

    def trip_id_id(self):
        trip = get_trip(
            origin_station_id="de:08111:6002",
            destination_station_id="de:08111:6118",
            check_time=self.get_next_monday_noon(),
        )
        self.assertIsNotNone(trip)
        self.assertIsInstance(trip, Trip)

    def test_start(self):
        print("e2e trips enum-enum")
        self.trips_enum_enum()
        print("e2e trip enum-enum")
        self.trip_enum_enum()
        print("e2e trips enum-id")
        self.trips_enum_id()
        print("e2e trip enum-id")
        self.trip_enum_id()
        print("e2e trips id-id")
        self.trips_id_id()
        print("e2e trip id-id")
        self.trip_id_id()
