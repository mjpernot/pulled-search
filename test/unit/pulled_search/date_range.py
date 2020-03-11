#!/usr/bin/python
# Classification (U)

"""Program:  date_range.py

    Description:  Unit testing of date_range in gen_libs.py.

    Usage:
        test/unit/pulled_search/date_range.py

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

        self.start_dt = datetime.datetime.strptime("20191011", "%Y%m%d")
        self.end_dt = datetime.datetime.strptime("20200309", "%Y%m%d")
        self.datelist = []
        self.dt1 = datetime.datetime.strptime("20191001", "%Y%m%d")
        self.dt2 = datetime.datetime.strptime("20191101", "%Y%m%d")
        self.dt3 = datetime.datetime.strptime("20191201", "%Y%m%d")
        self.dt4 = datetime.datetime.strptime("20200101", "%Y%m%d")
        self.dt5 = datetime.datetime.strptime("20200201", "%Y%m%d")
        self.dt6 = datetime.datetime.strptime("20200301", "%Y%m%d")
        self.results = [self.dt1.date(), self.dt2.date(), self.dt3.date(),
                        self.dt4.date(), self.dt5.date(), self.dt6.date()]

    def test_month_days(self):

        """Function:  test_month_days

        Description:  Test months_days function.

        Arguments:

        """

        for x in pulled_search.date_range(self.start_dt, self.end_dt):
            self.datelist.append(x)

        self.assertEqual(self.datelist, self.results)


if __name__ == "__main__":
    unittest.main()
