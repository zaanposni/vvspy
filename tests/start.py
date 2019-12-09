import unittest

from unittests import TestParser as test_a

# TODO: import new unittests in alphabetical order

tests = [test_a]

if __name__ == '__main__':
    print(f"Tests: {[x.__name__ for x in tests]}")
    print("================================================\n")
    unittest.main()
