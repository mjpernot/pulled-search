#!/usr/bin/python
# Classification (U)

"""Program:  get_archive_files.py

    Description:  Unit testing of get_archive_files in gen_libs.py.

    Usage:
        test/unit/pulled_search/get_archive_files.py

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
        test_two_months -> Test with data from two months.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.archive_dir = "/dir/archive"
        self.cmd = "command"
        self.pubdate = "20200210"
        self.cmd_regex = "Regular expression"
        self.now_dt = datetime.datetime.now()
        self.now_dt.replace(day=10)
        self.now_dt.replace(month=3)
        self.now_dt.replace(year=2020)
        self.dt1 = datetime.datetime.strptime("20200201", "%Y%m%d")
        self.dt2 = datetime.datetime.strptime("20200301", "%Y%m%d")
        self.range = [self.dt1.date(), self.dt2.date()]
        self.range2 = [self.dt1.date()]
        self.subresult1 = ["/dir/archive/command/2020/02/file1.txt",
                           "/dir/archive/command/2020/02/file2.txt"]
        self.subresult2 = ["/dir/archive/command/2020/03/file3.txt",
                           "/dir/archive/command/2020/03/file4.txt"]
        self.results = []
        self.results = self.results + self.subresult1
        self.results = self.results + self.subresult2
        self.results2 = []
        self.results2 = self.results2 + self.subresult1

    @mock.patch("pulled_search.gen_libs.filename_search")
    @mock.patch("pulled_search.gen_libs.date_range")
    @mock.patch("pulled_search.datetime.datetime")
    def test_one_month(self, mock_now, mock_range, mock_search):

        """Function:  test_one_month

        Description:  Test with data from one month.

        Arguments:

        """

        mock_now.now.return_value = self.now_dt
        mock_range.return_value = self.range2
        mock_search.return_value = self.subresult1

        self.assertEqual(
            pulled_search.get_archive_files(self.archive_dir, self.cmd,
                                            self.pubdate, self.cmd_regex),
            self.results2)

    @mock.patch("pulled_search.gen_libs.filename_search")
    @mock.patch("pulled_search.gen_libs.date_range")
    @mock.patch("pulled_search.datetime.datetime")
    def test_two_months(self, mock_now, mock_range, mock_search):

        """Function:  test_two_months

        Description:  Test with data from two months.

        Arguments:

        """

        mock_now.now.return_value = self.now_dt
        mock_range.return_value = self.range
        mock_search.side_effect = [self.subresult1, self.subresult2]

        self.assertEqual(
            pulled_search.get_archive_files(self.archive_dir, self.cmd,
                                            self.pubdate, self.cmd_regex),
            self.results)


if __name__ == "__main__":
    unittest.main()
