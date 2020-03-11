#!/usr/bin/python
# Classification (U)

"""Program:  month_days.py

    Description:  Unit testing of month_days in gen_libs.py.

    Usage:
        test/unit/pulled_search/month_days.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
from __future__ import print_function
import sys
import os
import datetime

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

# Third-party
import mock

# Local
sys.path.append(os.getcwd())
import pulled_search
import version

__version__ = version.__version__


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Unit testing initilization.
        test_month_days -> Test months_days function.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.dt = datetime.datetime.strptime("20200301", "%Y%m%d")
        self.results = 31

    def test_month_days(self):

        """Function:  test_month_days

        Description:  Test months_days function.

        Arguments:

        """

        self.assertEqual(pulled_search.month_days(self.dt), self.results)


if __name__ == "__main__":
    unittest.main()
