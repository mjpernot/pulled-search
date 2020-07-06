#!/usr/bin/python
# Classification (U)

"""Program:  mvalidate_dirs.py

    Description:  Unit testing of mvalidate_dirs in pulled_search.py.

    Usage:
        test/unit/pulled_search/mvalidate_dirs.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

# Third-party
import mock

# Local
sys.path.append(os.getcwd())
import pulled_search
import lib.gen_libs as gen_libs
import version

__version__ = version.__version__


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Initialize testing environment.
        test_archive_dir_failure -> Test with failure on archive_dir check.
        test_multiple_failures -> Test with multiple failures.
        test_error_dir_failure -> Test with failure on error_dir check.
        test_monitor_dir_failure -> Test with failure on monitor_dir check.
        test_no_failures -> Test with no failures on directory checks.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        class CfgTest(object):

            """Class:  CfgTest

            Description:  Class which is a representation of a cfg module.

            Methods:
                __init__ -> Initialize configuration environment.

            """

            def __init__(self):

                """Method:  __init__

                Description:  Initialization instance of the CfgTest class.

                Arguments:

                """

                self.monitor_dir = "/dir_path/monitor_dir"
                self.merror_dir = "/dir_path/error_dir"
                self.marchive_dir = "/dir_path/archive_dir"

        self.cfg = CfgTest()
        self.monitorkey = "/dir_path/monitor_dir"
        self.errorkey = "/dir_path/error_dir"
        self.monitorval = "Monitor_dir failure"
        self.errorval = "Error_dir failure"
        self.results2 = {self.monitorkey: self.monitorval}
        self.results4 = {"/dir_path/outfile_dir": "Outfile failure"}
        self.results5 = {self.errorkey: self.errorval}
        self.results6 = {self.monitorkey: self.monitorval,
                         self.errorkey: self.errorval}
        self.results7 = {"/dir_path/archive_dir": "Archive_dir failure"}
        self.chk = (True, None)
        self.chk2 = (False, self.monitorval)
        self.chk4 = (False, "Outfile failure")
        self.chk5 = (False, self.errorval)
        self.chk7 = (False, "Archive_dir failure")

    @mock.patch("pulled_search.gen_libs.chk_crt_dir")
    def test_archive_dir_failure(self, mock_chk):

        """Function:  test_archive_dir_failure

        Description:  Test with failure on archive_dir check.

        Arguments:

        """

        mock_chk.side_effect = [self.chk, self.chk, self.chk7]

        self.assertEqual(pulled_search.mvalidate_dirs(self.cfg), self.results7)

    @mock.patch("pulled_search.gen_libs.chk_crt_dir")
    def test_multiple_failures(self, mock_chk):

        """Function:  test_multiple_failures

        Description:  Test with multiple failures.

        Arguments:

        """

        mock_chk.side_effect = [self.chk2, self.chk5, self.chk]

        self.assertEqual(pulled_search.mvalidate_dirs(self.cfg), self.results6)

    @mock.patch("pulled_search.gen_libs.chk_crt_dir")
    def test_error_dir_failure(self, mock_chk):

        """Function:  test_error_dir_failure

        Description:  Test with failure on error_dir check.

        Arguments:

        """

        mock_chk.side_effect = [self.chk, self.chk5, self.chk]

        self.assertEqual(pulled_search.mvalidate_dirs(self.cfg), self.results5)

    @mock.patch("pulled_search.gen_libs.chk_crt_dir")
    def test_monitor_dir_failure(self, mock_chk):

        """Function:  test_monitor_dir_failure

        Description:  Test with failure on monitor_dir check.

        Arguments:

        """

        mock_chk.side_effect = [self.chk2, self.chk, self.chk]

        self.assertEqual(pulled_search.mvalidate_dirs(self.cfg), self.results2)

    @mock.patch("pulled_search.gen_libs.chk_crt_dir")
    def test_no_failures(self, mock_chk):

        """Function:  test_no_failures

        Description:  Test with no failures on directory checks.

        Arguments:

        """

        mock_chk.side_effect = [self.chk, self.chk, self.chk]

        self.assertEqual(pulled_search.mvalidate_dirs(self.cfg), {})


if __name__ == "__main__":
    unittest.main()
