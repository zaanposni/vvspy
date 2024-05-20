import unittest

from unittests import TestParser as test_a
from e2e import TripE2E as test_b
from e2e import ArrivalE2E as test_c
from e2e import DepartureE2E as test_d

tests = [test_a, test_b, test_c, test_d]

if __name__ == "__main__":
    print(f"Tests: {[x.__name__ for x in tests]}")
    print("================================================\n")
    unittest.main()
