import unittest
import sys
import os.path
import json

sys.path.append("..")

from vvspy.trip import _parse_response as parse_trip_response
from vvspy.arrivals import _parse_response as parse_arrival_response
from vvspy.departures import _parse_response as parse_departure_response
from vvspy.models import Trip
from vvspy.models import Arrival
from vvspy.models import Departure

path = os.path.join(".", "mock_results")


class TestParser(unittest.TestCase):
    def trip_200(self):
        with open(os.path.join(path, "trip_request_200.json"), "r") as f:
            data = json.load(f)
        results = parse_trip_response(data)
        self.assertTrue(results)
        self.assertTrue(all([isinstance(x, Trip) for x in results]))
        self.assertEqual(results[0].connections[0].origin.delay, 1)

    def trip_400(self):
        with open(os.path.join(path, "trip_request_400.json"), "r") as f:
            data = json.load(f)
        results = parse_trip_response(data)
        self.assertEqual(results, [])

    def arrival_200(self):
        with open(os.path.join(path, "arrival_request_200.json"), "r") as f:
            data = json.load(f)
        results = parse_arrival_response(data)
        self.assertTrue(results)
        self.assertTrue(all([isinstance(x, Arrival) for x in results]))
        self.assertEqual(results[0].delay, 1)

    def arrival_400(self):
        with open(os.path.join(path, "arrival_request_400.json"), "r") as f:
            data = json.load(f)
        results = parse_arrival_response(data)
        self.assertEqual(results, [])

    def departure_200(self):
        with open(os.path.join(path, "departure_request_200.json"), "r") as f:
            data = json.load(f)
        results = parse_departure_response(data)
        self.assertTrue(results)
        self.assertTrue(all([isinstance(x, Departure) for x in results]))
        self.assertEqual(results[0].delay, 1)

    def departure_400(self):
        with open(os.path.join(path, "departure_request_400.json"), "r") as f:
            data = json.load(f)
        results = parse_departure_response(data)
        self.assertEqual(results, [])

    def test_start(self):
        # ===========================================================================
        print("Test trip parser (200 mock result)")
        self.trip_200()

        # ===========================================================================
        print("Test trip parser (400 mock result)")
        self.trip_400()

        # ===========================================================================
        print("Test arrival parser (200 mock result)")
        self.arrival_200()

        # ===========================================================================
        print("Test arrival parser (400 mock result)")
        self.arrival_400()

        # ===========================================================================
        print("Test departure parser (200 mock result)")
        self.departure_200()

        # ===========================================================================
        print("Test departure parser (400 mock result)")
        self.departure_400()
