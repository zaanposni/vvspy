import json
from pathlib import Path

from vvspy.arrivals import _parse_arrivals as parse_arrivals
from vvspy.departures import _parse_departures as parse_departures
from vvspy.obj.arrival import Arrival
from vvspy.obj.departure import Departure
from vvspy.obj.trip import Trip
from vvspy.trips import _parse_trips as parse_trips

path = Path("tests/mock_results")


def test_trip_200():
    """Lorem ipsum"""
    with open(path / "trip_request_200.json", encoding="utf-8") as file:
        data = json.load(file)
    results = parse_trips(data, limit=100)
    assert results is not None
    assert all(isinstance(x, Trip) for x in results) is True
    assert results[0].connections[0].origin.delay == 1


def test_trip_400():
    """Lorem ipsum"""
    with open(path / "trip_request_400.json", encoding="utf-8") as file:
        data = json.load(file)
    results = parse_trips(data, limit=100)
    assert not results


def test_arrival_200():
    """Lorem ipsum"""
    with open(path / "arrival_request_200.json", encoding="utf-8") as file:
        data = json.load(file)
    results = parse_arrivals(data, limit=100)
    assert results is not None
    assert all(isinstance(x, Arrival) for x in results) is True
    assert results[0].delay == 1


def test_arrival_400():
    """Lorem ipsum"""
    with open(path / "arrival_request_400.json", encoding="utf-8") as file:
        data = json.load(file)
    results = parse_arrivals(data, limit=100)
    assert not results


def test_departure_200():
    """Lorem ipsum"""
    with open(path / "departure_request_200.json", encoding="utf-8") as file:
        data = json.load(file)
    results = parse_departures(data, limit=100)
    assert results is not None
    assert all(isinstance(x, Departure) for x in results) is True
    assert results[0].delay == 1


def test_departure_400():
    """Lorem ipsum"""
    with open(path / "departure_request_400.json", encoding="utf-8") as file:
        data = json.load(file)
    results = parse_departures(data, limit=100)
    assert not results
