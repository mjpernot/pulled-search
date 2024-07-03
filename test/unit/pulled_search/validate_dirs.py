# Classification (U)

"""Program:  validate_dirs.py

    Description:  Unit testing of validate_dirs in pulled_search.py.

    Usage:
        test/unit/pulled_search/validate_dirs.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os
import unittest
import mock

# Local
sys.path.append(os.getcwd())
import pulled_search
import version

__version__ = version.__version__


class CfgTest(object):

    """Class:  CfgTest

    Description:  Class which is a representation of a cfg module.

    Methods:
        __init__

    """

    def __init__(self):

        """Method:  __init__

        Description:  Initialization instance of the CfgTest class.

        Arguments:

        """

        self.log_dir = "/dir_path/log_dir"
        self.outfile = "/dir_path/outfile_dir/outfile"
        self.error_dir = "/dir_path/error_dir"
        self.processed_file = "/dir_path/processed_dir/processed_file"
        self.unparsable_dir = "/dir_path/unparsable_dir"
        self.raw_archive_dir = "/dir_path/raw_archive_dir"


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_raw_archive_dir_fail
        test_unparsable_dir_fail
        test_process_dir_fail
        test_multiple_failures
        test_error_dir_failure
        test_outfile_failure
        test_log_dir_failure
        test_no_failures

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.cfg = CfgTest()
        self.errdir = "/dir_path/error_dir"
        self.errval = "Error_dir failure"
        self.logdir ="/dir_path/log_dir"
        self.logval = "Log_dir failure"

        self.chk = (True, None)
        self.chk3 = (False, self.logval)
        self.chk4 = (False, "Outfile failure")
        self.chk5 = (False, self.errval)
        self.chk8 = (False, "Processed_dir failure")
        self.chk9 = (False, "Unparsable_dir failure")
        self.chk10 = (False, "Raw_archive_dir failure")

        self.results = dict()
        self.results3 = {self.logdir: self.logval}
        self.results4 = {"/dir_path/outfile_dir": "Outfile failure"}
        self.results5 = {self.errdir: self.errval}
        self.results6 = {self.logdir: self.logval, self.errdir: self.errval}
        self.results8 = {"/dir_path/processed_dir": "Processed_dir failure"}
        self.results9 = {"/dir_path/unparsable_dir": "Unparsable_dir failure"}
        self.results10 = {
            "/dir_path/raw_archive_dir": "Raw_archive_dir failure"}

    @mock.patch("pulled_search.gen_libs.chk_crt_dir")
    def test_raw_archive_dir_fail(self, mock_chk):

        """Function:  test_raw_archive_dir_fail

        Description:  Test with failure on raw_archive_dir directory.

        Arguments:

        """

        mock_chk.side_effect = [
            self.chk, self.chk, self.chk, self.chk, self.chk, self.chk10]

        self.assertEqual(pulled_search.validate_dirs(self.cfg), self.results10)

    @mock.patch("pulled_search.gen_libs.chk_crt_dir")
    def test_unparsable_dir_fail(self, mock_chk):

        """Function:  test_unparsable_dir_fail

        Description:  Test with failure on unparsable_dir directory.

        Arguments:

        """

        mock_chk.side_effect = [
            self.chk, self.chk, self.chk, self.chk, self.chk9, self.chk]

        self.assertEqual(pulled_search.validate_dirs(self.cfg), self.results9)

    @mock.patch("pulled_search.gen_libs.chk_crt_dir")
    def test_process_dir_fail(self, mock_chk):

        """Function:  test_process_dir_fail

        Description:  Test with failure on processed_dir directory.

        Arguments:

        """

        mock_chk.side_effect = [
            self.chk, self.chk, self.chk, self.chk8, self.chk, self.chk]

        self.assertEqual(pulled_search.validate_dirs(self.cfg), self.results8)

    @mock.patch("pulled_search.gen_libs.chk_crt_dir")
    def test_multiple_failures(self, mock_chk):

        """Function:  test_multiple_failures

        Description:  Test with multiple failures.

        Arguments:

        """

        mock_chk.side_effect = [
            self.chk3, self.chk, self.chk5, self.chk, self.chk, self.chk]

        self.assertEqual(pulled_search.validate_dirs(self.cfg), self.results6)

    @mock.patch("pulled_search.gen_libs.chk_crt_dir")
    def test_error_dir_failure(self, mock_chk):

        """Function:  test_error_dir_failure

        Description:  Test with failure on error_dir check.

        Arguments:

        """

        mock_chk.side_effect = [
            self.chk, self.chk, self.chk5, self.chk, self.chk, self.chk]

        self.assertEqual(pulled_search.validate_dirs(self.cfg), self.results5)

    @mock.patch("pulled_search.gen_libs.chk_crt_dir")
    def test_outfile_failure(self, mock_chk):

        """Function:  test_outfile_failure

        Description:  Test with failure on outfile check.

        Arguments:

        """

        mock_chk.side_effect = [
            self.chk, self.chk4, self.chk, self.chk, self.chk, self.chk]

        self.assertEqual(pulled_search.validate_dirs(self.cfg), self.results4)

    @mock.patch("pulled_search.gen_libs.chk_crt_dir")
    def test_log_dir_failure(self, mock_chk):

        """Function:  test_log_dir_failure

        Description:  Test with failure on log_dir check.

        Arguments:

        """

        mock_chk.side_effect = [
            self.chk3, self.chk, self.chk, self.chk, self.chk, self.chk]

        self.assertEqual(pulled_search.validate_dirs(self.cfg), self.results3)

    @mock.patch("pulled_search.gen_libs.chk_crt_dir")
    def test_no_failures(self, mock_chk):

        """Function:  test_no_failures

        Description:  Test with no failures on directory checks.

        Arguments:

        """

        mock_chk.side_effect = [
            self.chk, self.chk, self.chk, self.chk, self.chk, self.chk]

        self.assertEqual(pulled_search.validate_dirs(self.cfg), self.results)


if __name__ == "__main__":
    unittest.main()
